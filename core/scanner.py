import platform
import subprocess


class WiFiScanner:
  """Handles cross-platform scanning of nearby Wi-Fi networks."""

  @staticmethod
  def scan_networks():
    system = platform.system()
    networks = []

    if system == "Windows":
      networks = WiFiScanner._scan_windows()
    elif system == "Linux":
      networks = WiFiScanner._scan_linux()
    elif system == "Darwin":
      networks = WiFiScanner._scan_macos()
    else:
      print(f"[Warning] Unsupported platform for live Wi-Fi scan: {system}")

    return networks

  @staticmethod
  def _scan_windows():
    networks = []
    try:
      # Use mode=bssid which is universally supported across all Windows versions
      output = subprocess.check_output(
          ["netsh", "wlan", "show", "networks", "mode=bssid"],
          encoding="utf-8",
          errors="ignore",
      )

      current_ssid = "Unknown"
      current_security = "Open"
      current_bssid = ""
      current_signal = -70
      current_channel = 1

      for line in output.splitlines():
        line = line.strip()

        if line.startswith("SSID"):
          parts = line.split(":", 1)
          if len(parts) > 1:
            val = parts[1].strip()
            if val:
              current_ssid = val

        elif line.startswith("Authentication"):
          parts = line.split(":", 1)
          if len(parts) > 1:
            current_security = parts[1].strip()

        elif line.startswith("BSSID"):
          # If we were tracking a previous BSSID, save it before starting a new one
          if current_bssid:
            networks.append({
                "ssid": current_ssid if current_ssid else "Hidden SSID",
                "bssid": current_bssid,
                "signal": current_signal,
                "channel": current_channel,
                "security": current_security,
            })
          parts = line.split(":", 1)
          if len(parts) > 1:
            current_bssid = parts[1].strip()

        elif line.startswith("Signal"):
          parts = line.split(":", 1)
          if len(parts) > 1:
            sig_str = parts[1].strip().replace("%", "")
            try:
              percent = int(sig_str)
              current_signal = int((percent / 2) - 100)
            except ValueError:
              current_signal = -70

        elif line.startswith("Channel"):
          parts = line.split(":", 1)
          if len(parts) > 1:
            try:
              current_channel = int(parts[1].strip())
            except ValueError:
              current_channel = 1

      # Append the last remaining network record
      if current_bssid:
        networks.append({
            "ssid": current_ssid if current_ssid else "Hidden SSID",
            "bssid": current_bssid,
            "signal": current_signal,
            "channel": current_channel,
            "security": current_security,
        })

    except Exception as e:
      print(f"[Error] Windows Wi-Fi scan failed: {e}")

    return networks

  @staticmethod
  def _scan_linux():
    networks = []
    try:
      output = subprocess.check_output(
          ["nmcli", "-t", "-f", "SSID,BSSID,SIGNAL,CHAN,SECURITY", "dev", "wifi"],
          encoding="utf-8",
          errors="ignore",
      )
      for line in output.splitlines():
        parts = line.split(":")
        if len(parts) >= 5:
          sig_pct = int(parts[2]) if parts[2].isdigit() else 50
          dbm = int((sig_pct / 2) - 100)
          networks.append({
              "ssid": parts[0] or "Hidden SSID",
              "bssid": parts[1],
              "signal": dbm,
              "channel": int(parts[3]) if parts[3].isdigit() else 1,
              "security": parts[4],
          })
    except Exception as e:
      print(f"[Error] Linux Wi-Fi scan failed: {e}")
    return networks

  @staticmethod
  def _scan_macos():
    networks = []
    try:
      airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
      output = subprocess.check_output(
          [airport_path, "-s"], encoding="utf-8", errors="ignore"
      )
      for line in output.splitlines()[1:]:
        parts = line.strip().split()
        if len(parts) >= 3:
          ssid = parts[0]
          bssid = parts[1]
          try:
            rssi = int(parts[2])
          except ValueError:
            rssi = -70
          networks.append({
              "ssid": ssid,
              "bssid": bssid,
              "signal": rssi,
              "channel": 1,
              "security": "Unknown",
          })
    except Exception as e:
      print(f"[Error] macOS Wi-Fi scan failed: {e}")
    return networks