import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import config


class SparklinePanel(ctk.CTkFrame):
  """Panel displaying historical signal strength sparkline chart for selected Wi-Fi node."""

  def __init__(self, parent, db_manager, **kwargs):
    super().__init__(
        parent, fg_color=config.THEME_COLORS["bg_dark"], corner_radius=10, **kwargs
    )
    self.db = db_manager

    # Title label
    self.header_label = ctk.CTkLabel(
        self,
        text="Signal History (Select a Node)",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=config.THEME_COLORS["text_light"],
    )
    self.header_label.pack(padx=10, pady=(10, 5), anchor="w")

    # Setup Matplotlib Figure
    self.fig = Figure(figsize=(4, 2.5), dpi=80)
    self.fig.patch.set_facecolor(config.THEME_COLORS["bg_dark"])

    self.ax = self.fig.add_subplot(111)
    self._style_axis("No Network Selected")

    self.canvas = FigureCanvasTkAgg(self.fig, master=self)
    self.canvas.get_tk_widget().pack(
        padx=5, pady=5, fill="both", expand=True
    )

  def _style_axis(self, title_text):
    self.ax.clear()
    self.ax.set_facecolor(config.THEME_COLORS["card_bg"])
    self.ax.set_title(
        title_text, color=config.THEME_COLORS["text_light"], fontsize=10
    )
    self.ax.tick_params(colors=config.THEME_COLORS["text_muted"], labelsize=8)
    for spine in self.ax.spines.values():
      spine.set_color(config.THEME_COLORS["grid_line"])
    self.ax.grid(True, color=config.THEME_COLORS["grid_line"], linestyle="--", alpha=0.5)

  def load_bssid(self, bssid, ssid):
    self.header_label.configure(text=f"History: {ssid} ({bssid})")
    records = self.db.get_history_for_bssid(bssid, limit=30)

    self._style_axis(f"Signal Strength over Time")

    if not records:
      self.canvas.draw()
      return

    # records are returned as (timestamp, signal) ordered DESC, reverse for chronological
    records.reverse()
    timestamps = [r[0].split(" ")[1] for r in records]  # Time portion only
    signals = [r[1] for r in records]

    self.ax.plot(
        timestamps,
        signals,
        color=config.THEME_COLORS["accent_green"],
        marker="o",
        linewidth=2,
        markersize=4,
    )
    self.ax.set_ylabel("dBm", color=config.THEME_COLORS["text_muted"], fontsize=8)
    self.ax.tick_params(axis="x", rotation=30)
    self.fig.tight_layout()
    self.canvas.draw()