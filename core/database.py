import sqlite3
import os
from datetime import datetime


class DatabaseManager:
  """Handles SQLite database operations for Wi-Fi signal history logging."""

  def __init__(self, db_path="wifi_radar.db"):
    self.db_path = db_path
    self.init_db()

  def get_connection(self):
    return sqlite3.connect(self.db_path)

  def init_db(self):
    """Initializes the SQLite scan history table if it doesn't exist."""
    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    ssid TEXT,
                    bssid TEXT,
                    signal INTEGER,
                    channel INTEGER,
                    security TEXT
                )
            """)
      conn.commit()

  def save_scan_results(self, networks):
    """Saves a batch of discovered Wi-Fi networks to the database."""
    if not networks:
      return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with self.get_connection() as conn:
      cursor = conn.cursor()
      for net in networks:
        cursor.execute(
            """
                    INSERT INTO scan_history (timestamp, ssid, bssid, signal, channel, security)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
            (
                timestamp,
                net.get("ssid", "Unknown"),
                net.get("bssid", "N/A"),
                net.get("signal", -100),
                net.get("channel", 0),
                net.get("security", "Open"),
            ),
        )
      conn.commit()
  def get_history_for_bssid(self, bssid, limit=50):
    """Retrieves historical signal readings for a specific BSSID (for sparklines)."""
    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute(
          """
                SELECT timestamp, signal FROM scan_history
                WHERE bssid = ?
                ORDER BY id DESC LIMIT ?
            """,
          (bssid, limit),
      )
      return cursor.fetchall()