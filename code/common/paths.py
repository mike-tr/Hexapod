from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent     # -> Hexapod/

DATA = ROOT / "data"
IMAGES = DATA / "calibration"
CONFIG = ROOT / "config"

print("Root :", ROOT, "\nData", DATA, "\nCalib_images", IMAGES, "\nConfig", CONFIG)