import csv
import json
import os
from datetime import datetime


class DataExporter:
  """Handles exporting Wi-Fi scan results to CSV and JSON formats."""

  @staticmethod
  def export_to_csv(scan_data, filepath=None):
    """Exports a list of network dictionaries to a CSV file."""
    if not scan_data:
      return False, "No scan data available to export."

    if not filepath:
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      filepath = f"wifi_scan_log_{timestamp}.csv"

    try:
      fieldnames = list(scan_data[0].keys())

      with open(filepath, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in scan_data:
          writer.writerow(row)

      return True, filepath
    except Exception as e:
      return False, str(e)

  @staticmethod
  def export_to_json(scan_data, filepath=None):
    """Exports a list of network dictionaries to a JSON file."""
    if not scan_data:
      return False, "No scan data available to export."

    if not filepath:
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      filepath = f"wifi_scan_log_{timestamp}.json"

    try:
      with open(filepath, mode="w", encoding="utf-8") as json_file:
        json.dump(scan_data, json_file, indent=4, default=str)

      return True, json_file.name

    except Exception as e:
      return False, str(e)