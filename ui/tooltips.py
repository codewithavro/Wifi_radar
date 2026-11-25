import tkinter as tk


class ToolTip:
  """Provides interactive hover tooltips for canvas elements or UI widgets."""

  def __init__(self, widget, text_func):
    self.widget = widget
    self.text_func = text_func
    self.tip_window = None
    self.id = None
    self.x = self.y = 0

    self.widget.bind("<Enter>", self.enter)
    self.widget.bind("<Leave>", self.leave)
    self.widget.bind("<Motion>", self.motion)

  def enter(self, event=None):
    self.schedule()

  def leave(self, event=None):
    self.unschedule()
    self.hide_tip()

  def motion(self, event=None):
    self.x = event.x_root + 15
    self.y = event.y_root + 10

  def schedule(self):
    self.unschedule()
    self.id = self.widget.after(500, self.show_tip)

  def unschedule(self):
    id = self.id
    self.id = None
    if id:
      self.widget.after_cancel(id)

  def show_tip(self, event=None):
    text = self.text_func()
    if not text:
      return

    x = self.x
    y = self.y
    self.tip_window = tw = tk.Toplevel(self.widget)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")

    label = tk.Label(
        tw,
        text=text,
        justify=tk.LEFT,
        background="#1F2937",
        foreground="#F3F4F6",
        relief=tk.SOLID,
        borderwidth=1,
        font=("Arial", 9, "normal"),
        padx=6,
        pady=4,
    )
    label.pack(ipadx=1)

  def hide_tip(self):
    tw = self.tip_window
    self.tip_window = None
    if tw:
      tw.destroy()