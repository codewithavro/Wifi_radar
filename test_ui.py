"""Standalone test script for Wi-Radar UI components."""

from ui import MainWindow


def run_ui_test():
  # Initialize the main application window
  app = MainWindow()

  # Create mock Wi-Fi scan data to test the radar and sparkline panels
  mock_networks = [
      {
          "ssid": "Home_Fiber_5G",
          "bssid": "AA:BB:CC:11:22:33",
          "signal": -42,
          "channel": 36,
          "security": "WPA3",
      },
      {
          "ssid": "Neighbor_Network",
          "bssid": "DD:EE:FF:44:55:66",
          "signal": -68,
          "channel": 6,
          "security": "WPA2",
      },
      {
          "ssid": "Public_Guest_WiFi",
          "bssid": "12:34:56:78:90:AB",
          "signal": -82,
          "channel": 11,
          "security": "Open",
      },
      {
          "ssid": "IoT_SmartHome",
          "bssid": "FA:CE:BO:OK:00:01",
          "signal": -55,
          "channel": 1,
          "security": "WPA2",
      },
  ]

  # Inject mock data into the UI and database history
  print("[Test] Injecting mock network data into UI...")
  app.db.save_scan_results(mock_networks)
  app.on_scan_update(mock_networks)

  # Start the Tkinter GUI main loop
  app.mainloop()


if __name__ == "__main__":
  run_ui_test()