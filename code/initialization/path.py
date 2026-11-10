from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent     # -> Hexapod/
print("Root :", ROOT)
CALIB = ROOT / "calibration"
IMAGES = CALIB / "images"
CONFIG = ROOT / "config"