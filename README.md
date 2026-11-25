Wi-Fi Radar

A real-time Python desktop application for scanning, visualizing, and logging nearby Wi-Fi networks with an interactive radar display, sonar audio feedback, signal sparklines, SQLite persistence, and data export.

Features

Live Radar Visualization: Plots detected Wi-Fi networks on an animated radar canvas based on signal strength (RSSI) and channel/band characteristics.

Real-Time Signal Sparklines: Displays historical signal stability and fluctuations for selected networks in a dedicated sparkline panel.

Sonar Audio Feedback: Plays customizable sonar ping cues synchronized with radar sweeps and network detection events.

Interactive Network Tooltips: Hover over radar blips to inspect SSID, BSSID, signal strength, channel, and security details.

SQLite Scan Logging: Automatically records scan sessions and signal history into a local SQLite database (wifi_radar.db).

Data Export: Export captured network metrics and scan logs for external analysis.

Threaded Background Scanning: Uses background worker threads so live scanning never freezes the user interface.

Prerequisites

Operating System: Windows 10 / 11 (uses native wireless scanning utilities)

Python: Python 3.9 or higher

Wi-Fi Adapter: Active wireless network interface

Installation

Clone the repository:

git clone https://github.com/codewithavro/Wifi_radar.git
cd Wifi_radar


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


(If requirements.txt is not present, install the GUI framework used by the project, such as PyQt6 or PySide6.)

Usage

Launch the main application from your activated virtual environment:

python main.py


To run the UI test suite or standalone interface check:

python test_ui.py


Configuration

Application defaults—such as scan intervals, radar sweep speed, audio toggle settings, and database paths—can be adjusted in config.py.

License

This project is open source and available under the MIT License.
