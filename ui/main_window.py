import os
import customtkinter as ctk
from audio import SoundManager
from core import DatabaseManager, ScanWorker
from data_export import DataExporter
import config
from .radar_canvas import RadarCanvas
from .sparkline_panel import SparklinePanel


class MainWindow(ctk.CTk):
  """Main application window for Wi-Radar."""

  def __init__(self):
    super().__init__()

    self.title(config.WINDOW_TITLE)
    self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    self.minsize(950, 650)

    # Set theme colors
    ctk.set_appearance_mode("Dark")
    self.configure(fg_color=config.THEME_COLORS["bg_dark"])

    # Initialize Managers & Workers
    self.db = DatabaseManager()
    self.sound_manager = SoundManager()
    self.latest_networks = []
    self.worker = ScanWorker(
        callback=self.on_scan_update, interval=config.DEFAULT_SCAN_INTERVAL
    )

    # Load Window Icon if available
    icon_path = "assets/icon.ico"
    if os.path.exists(icon_path):
      try:
        self.iconbitmap(icon_path)
      except Exception:
        pass

    self._build_layout()

    # Start automatic background scanning thread
    self.worker.start()

  def _build_layout(self):
    # Main container grid
    self.grid_columnconfigure(0, weight=3)  # Radar area
    self.grid_columnconfigure(1, weight=2)  # Control & Sparkline panel
    self.grid_rowconfigure(0, weight=1)

    # --- Left Pane: Radar Display & Status ---
    left_frame = ctk.CTkFrame(
        self, fg_color=config.THEME_COLORS["card_bg"], corner_radius=12
    )
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    self.radar_canvas = RadarCanvas(
        left_frame, on_node_click=self.on_node_selected
    )
    self.radar_canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # --- Right Pane: Controls, Info & Sparkline ---
    right_frame = ctk.CTkFrame(
        self, fg_color=config.THEME_COLORS["card_bg"], corner_radius=12
    )
    right_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
    right_frame.grid_rowconfigure(2, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Header / Title
    title_label = ctk.CTkLabel(
        right_frame,
        text=config.APP_NAME,
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color=config.THEME_COLORS["accent_green"],
    )
    title_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

    # Control Buttons Frame
    btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    btn_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
    btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

    self.scan_btn = ctk.CTkButton(
        btn_frame,
        text="Stop Scan",
        fg_color="#EF4444",
        hover_color="#DC2626",
        command=self.toggle_scan,
    )
    self.scan_btn.grid(row=0, column=0, padx=2, pady=5, sticky="ew")

    csv_btn = ctk.CTkButton(
        btn_frame,
        text="Export CSV",
        fg_color=config.THEME_COLORS["accent_cyan"],
        hover_color="#0891B2",
        text_color="#000000",
        command=self.export_csv,
    )
    csv_btn.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

    json_btn = ctk.CTkButton(
        btn_frame,
        text="Export JSON",
        fg_color=config.THEME_COLORS["accent_cyan"],
        hover_color="#0891B2",
        text_color="#000000",
        command=self.export_json,
    )
    json_btn.grid(row=0, column=2, padx=2, pady=5, sticky="ew")

    # Sparkline & Details Panel
    self.sparkline_panel = SparklinePanel(right_frame, db_manager=self.db)
    self.sparkline_panel.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

    # Status Bar
    self.status_label = ctk.CTkLabel(
        right_frame,
        text="Status: Scanning initialized...",
        font=ctk.CTkFont(size=11),
        text_color=config.THEME_COLORS["text_muted"],
    )
    self.status_label.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="w")

  def on_scan_update(self, networks):
    """Callback triggered whenever background scanner finishes a scan cycle."""
    self.latest_networks = networks
    # Safely update UI components from main thread
    self.after(0, self._update_ui_elements, networks)

  def _update_ui_elements(self, networks):
    count = len(networks)
    self.status_label.configure(
        text=f"Status: Found {count} networks. Live tracking active."
    )
    self.radar_canvas.update_networks(networks)

    # Trigger sonar audio ping if networks were discovered
    if count > 0:
      self.sound_manager.play_ping()

  def on_node_selected(self, network):
    """Triggered when user clicks a Wi-Fi node on the radar canvas."""
    if network and "bssid" in network:
      self.sparkline_panel.load_bssid(network["bssid"], network.get("ssid"))

  def toggle_scan(self):
    if self.worker.running:
      self.worker.stop()
      self.scan_btn.configure(
          text="Start Scan", fg_color="#10B981", hover_color="#059669"
      )
      self.status_label.configure(text="Status: Scanning paused.")
    else:
      self.worker.start()
      self.scan_btn.configure(
          text="Stop Scan", fg_color="#EF4444", hover_color="#DC2626"
      )
      self.status_label.configure(text="Status: Scanning resumed...")

  export_success_label = None

  def export_csv(self):
    success, filepath = DataExporter.export_to_csv(self.latest_networks)
    if success:
      self.status_label.configure(text=f"Exported CSV: {filepath}")
    else:
      self.status_label.configure(text=f"Export failed: {filepath}")

  def export_json(self):
    success, filepath = DataExporter.export_to_json(self.latest_networks)
    if success:
      self.status_label.configure(text=f"Exported JSON: {filepath}")
    else:
      self.status_label.configure(text=f"Export failed: {filepath}")

  def destroy(self):
    self.worker.stop()
    super().destroy()