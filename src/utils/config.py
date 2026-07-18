"""
Project Configuration
AI-Powered Eye Controlled Communication System
"""

# ==========================================
# CAMERA SETTINGS
# ==========================================

CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# ==========================================
# BLINK SETTINGS
# ==========================================

EAR_THRESHOLD = 0.20

REQUIRED_FRAMES = 3

COOLDOWN = 0.50

SHORT_BLINK_MAX = 0.40

LONG_BLINK_MIN = 0.80

# ==========================================
# UI SETTINGS
# ==========================================

FONT_SCALE = 1
TEXT_THICKNESS = 2

MENU_START_X = 450
MENU_START_Y = 120
MENU_SPACING = 50

# ==========================================
# MENU OPTIONS
# ==========================================

MENU_OPTIONS = [
    "HELP",
    "WATER",
    "FOOD",
    "YES",
    "NO"
]

# ==========================================
# COLORS (BGR)
# ==========================================

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (0, 255, 255)