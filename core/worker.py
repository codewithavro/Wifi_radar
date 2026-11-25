import threading
import time
from .database import DatabaseManager
from .scanner import WiFiScanner


class ScanWorker:
  """Manages background threading for continuous non-blocking Wi-Fi scans."""

  def __init__(self, callback, interval=5):
    self.callback = callback
    self.interval = interval
    self.running = False
    self.thread = None
    self.db = DatabaseManager()

  def start(self):
    """Starts the background scanning thread."""
    if not self.running:
      self.running = True
      self.thread = threading.Thread(target=self._run_loop, daemon=True)
      self.thread.start()

  def stop(self):
    """Stops the background scanning thread gracefully."""
    self.running = False
    if self.thread:
      self.thread.join(timeout=1.0)

  def _run_loop(self):
    while self.running:
      try:
        networks = WiFiScanner.scan_networks()
        if networks:
          self.db.save_scan_results(networks)
        if self.callback:
          self.callback(networks)
      except Exception as e:
        print(f"[Error] Scan worker loop error: {e}")

      # Sleep in small increments to allow responsive application termination
      elapsed = 0
      while elapsed < self.interval and self.running:
        time.sleep(0.5)
        elapsed += 0.5