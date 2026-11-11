import json
import numpy as np
from dataclasses import dataclass

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.paths import CONFIG


@dataclass(frozen=True)
class Intrinsics:
    K: np.ndarray
    dist: np.ndarray
    width: int
    height: int


@dataclass(frozen=True)
class Extrinsics:
    height_mm: float
    tilt_deg: float
    forward_mm: float
    right_mm: float


def load_intrinsics(path=None) -> Intrinsics:
    d = np.load(str(path or CONFIG / "camera_intrinsics.npz"))
    w, h = d["size"]
    return Intrinsics(d["K"], d["dist"], int(w), int(h))


def load_extrinsics(path=None) -> Extrinsics:
    j = json.loads((path or CONFIG / "camera_extrinsics.json").read_text())
    return Extrinsics(j["height_mm"], j["tilt_deg"],
                      j["forward_mm"], j["right_mm"])


INTRINSICS = load_intrinsics()
EXTRINSICS = load_extrinsics()

K = INTRINSICS.K
DIST = INTRINSICS.dist