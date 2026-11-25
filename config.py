"""Global configuration parameters, color palettes, and constants for Wi-Radar."""

# Application Metadata
APP_NAME = "Wi-Radar"

WINDOW_TITLE = "Wi-Radar - Professional Wi-Fi Signal Visualizer"

WINDOW_WIDTH = 1100

WINDOW_HEIGHT = 750

# Scanning Configuration

DEFAULT_SCAN_INTERVAL = 5  # Seconds between background auto-refreshes

# Radar Theme & Color Palette (Dark Mode / Cyberpunk UI)
THEME_COLORS = {
    "bg_dark": "#0B0F19",

    "card_bg": "#111827",

    "accent_green": "#10B981",

    "accent_cyan": "#06B6D4",

    "text_light": "#F3F4F6",

    "text_muted": "#9CA3AF",

    "radar_sweep": "#00FF66",

    "grid_line": "#1F2937",

    "node_fill": "#3B82F6",

    "node_outline": "#60A5FA",
}

# Signal Strength Quality Thresholds (dBm)
SIGNAL_THRESHOLDS = {
    "EXCELLENT": -50,  # >= -50 dBm
    
    "GOOD": -65,  # >= -65 dBm
    
    "FAIR": -80,  # >= -80 dBm
    
    "POOR": -90,  # < -80 dBm
}