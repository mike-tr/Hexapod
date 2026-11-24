import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.camera_config import load_profile, CameraProfile


from common.vector import Vec3


profile = load_profile("stream")
print(profile)