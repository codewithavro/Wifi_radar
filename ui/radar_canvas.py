import math
import tkinter as tk
import config


class RadarCanvas(tk.Canvas):
  """Interactive radar display canvas for Wi-Fi signal mapping."""

  def __init__(self, parent, on_node_click=None, **kwargs):
    super().__init__(
        parent,
        bg=config.THEME_COLORS["bg_dark"],
        highlightthickness=0,
        **kwargs,
    )
    self.on_node_click = on_node_click
    self.networks = []
    self.sweep_angle = 0
    self.node_items = {}  # Maps canvas item ID to network dictionary

    self.bind("<Configure>", self._on_resize)
    self.bind("<Button-1>", self._on_canvas_click)

    # Start sweep animation loop
    self._animate_sweep()

  def _on_resize(self, event):
    self.width = event.width
    self.height = event.height
    self.center_x = self.width / 2
    self.center_y = self.height / 2
    self.max_radius = min(self.center_x, self.center_y) - 30
    self.redraw()

  def update_networks(self, networks):
    self.networks = networks
    self.redraw()

  def redraw(self):
    self.delete("radar_element")
    self.node_items.clear()

    if not hasattr(self, "center_x"):
      return

    # Draw concentric circles (Range rings: -30dBm, -50dBm, -70dBm, -90dBm)
    rings = 4
    for i in range(1, rings + 1):
      r = (self.max_radius / rings) * i
      self.create_oval(
          self.center_x - r,
          self.center_y - r,
          self.center_x + r,
          self.center_y + r,
          outline=config.THEME_COLORS["grid_line"],
          width=1,
          tags=("radar_element", "grid"),
      )

    # Draw crosshairs
    self.create_line(
        self.center_x - self.max_radius,
        self.center_y,
        self.center_x + self.max_radius,
        self.center_y,
        fill=config.THEME_COLORS["grid_line"],
        tags=("radar_element", "grid"),
    )
    self.create_line(
        self.center_x,
        self.center_y - self.max_radius,
        self.center_x,
        self.center_y + self.max_radius,
        fill=config.THEME_COLORS["grid_line"],
        tags=("radar_element", "grid"),
    )

    # Draw radar sweep line
    rad = math.radians(self.sweep_angle)
    end_x = self.center_x + self.max_radius * math.cos(rad)
    end_y = self.center_y + self.max_radius * math.sin(rad)
    self.create_line(
        self.center_x,
        self.center_y,
        end_x,
        end_y,
        fill=config.THEME_COLORS["radar_sweep"],
        width=2,
        tags=("radar_element", "sweep"),
    )

    # Plot networks as nodes
    for idx, net in enumerate(self.networks):
      signal = net.get("signal", -90)
      # Map signal (-30 dBm to -100 dBm) to radius
      sig_clamped = max(-100, min(-30, signal))
      norm_dist = (1.0 - (sig_clamped - (-100)) / 70.0)
      r = norm_dist * self.max_radius

      # Deterministic angle based on index or hash
      angle = (idx * 137.5) % 360
      rad_node = math.radians(angle)

      nx = self.center_x + r * math.cos(rad_node)
      ny = self.center_y + r * math.sin(rad_node)

      node_radius = 6
      node_item = self.create_oval(
          nx - node_radius,
          ny - node_radius,
          nx + node_radius,
          ny + node_radius,
          fill=config.THEME_COLORS["node_fill"],
          outline=config.THEME_COLORS["node_outline"],
          width=2,
          tags=("radar_element", "node"),
      )

      # Store mapping for click lookup
      self.node_items[node_item] = net

      # Draw SSID text label near node
      self.create_text(
          nx + 10,
          ny,
          text=net.get("ssid", "Unknown"),
          fill=config.THEME_COLORS["text_light"],
          anchor="w",
          font=("Arial", 9),
          tags=("radar_element", "label"),
      )

  def _animate_sweep(self):
    self.sweep_angle = (self.sweep_angle + 4) % 360
    if hasattr(self, "center_x"):
      self.redraw()
    self.after(50, self._animate_sweep)

  def _on_canvas_click(self, _event):
    clicked_items = self.find_withtag("current")
    for item in clicked_items:
      if item in self.node_items:
        net = self.node_items[item]
        if self.on_node_click:
          self.on_node_click(net)
        break