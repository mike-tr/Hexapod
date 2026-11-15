import json
import numpy as np
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.paths import CONFIG

_ACCEPTED_DIST_LEN = (4, 5, 8, 12, 14)   # what OpenCV's models allow


@dataclass(frozen=True)
class Capture:
    """How the sensor is sampled. Changing any field invalidates the intrinsics."""
    size: tuple[int, int]          # output frame (what K describes)
    raw_size: tuple[int, int]      # sensor mode -- pins the field of view
    lores: tuple[int, int]
    format: str
    format_lores: str
    hflip: bool
    vflip: bool

    @property
    def width(self) -> int:  return self.size[0]
    @property
    def height(self) -> int: return self.size[1]


@dataclass(frozen=True, eq=False)                 # eq=False: ndarray __eq__ is not a bool
class Intrinsics:
    K: np.ndarray                                 # 3x3
    dist: np.ndarray
    rms_px: float | None
    n_images: int
    square_mm: float | None
    calibrated_utc: str | None

    @property
    def calibrated(self) -> bool:
        return self.n_images > 0 and self.rms_px is not None

    @property
    def fx(self) -> float: return float(self.K[0, 0])
    @property
    def fy(self) -> float: return float(self.K[1, 1])
    @property
    def cx(self) -> float: return float(self.K[0, 2])
    @property
    def cy(self) -> float: return float(self.K[1, 2])

    def hfov_deg(self, width: int) -> float:
        return float(np.degrees(2 * np.arctan(width / (2 * self.fx))))


@dataclass(frozen=True, eq=False)
class CameraProfile:
    name: str
    capture: Capture
    intrinsics: Intrinsics

    def with_intrinsics(self, K, dist, *, rms_px, n_images, square_mm=None) -> "CameraProfile":
        """New profile, same capture block, fresh intrinsics. Stamps the time itself."""
        return replace(self, intrinsics=Intrinsics(
            K=np.asarray(K, float),
            dist=np.asarray(dist, float).ravel(),
            rms_px=float(rms_px),
            n_images=int(n_images),
            square_mm=square_mm if square_mm is not None else self.intrinsics.square_mm,
            calibrated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ))


@dataclass(frozen=True)
class Extrinsics:
    """Where the camera sits. Physical -- shared by every profile."""
    height_mm: float
    tilt_deg: float
    forward_mm: float
    right_mm: float


# ----------------------------------------------------------------- load / save

def load_profile(name: str, path: Path | None = None) -> CameraProfile:
    p = Path(path) if path else CONFIG / f"camera_{name}.json"
    j = json.loads(p.read_text())

    if j.get("profile") != name:
        raise ValueError(f"{p.name} declares profile {j.get('profile')!r}, expected {name!r}")

    c = j["capture"]
    cap = Capture(size=tuple(c["size"]), raw_size=tuple(c["raw_size"]), lores=tuple(c["lores"]),
                  format=c["format"], format_lores=c["format_lores"], hflip=bool(c["hflip"]), vflip=bool(c["vflip"]))

    i = j["intrinsics"]
    intr = Intrinsics(K=np.asarray(i["K"], dtype=float),
                      dist=np.asarray(i["dist"], dtype=float).ravel(),
                      rms_px=i.get("rms_px"), n_images=int(i.get("n_images", 0)),
                      square_mm=i.get("square_mm"), calibrated_utc=i.get("calibrated_utc"))

    _validate(name, cap, intr, p)
    return CameraProfile(name=name, capture=cap, intrinsics=intr)


def save_profile(prof: CameraProfile, path: Path | None = None) -> Path:
    """Write capture settings and intrinsics as ONE document. The calibration
    script must use this, so the two halves can never drift apart."""
    p = Path(path) if path else CONFIG / f"camera_{prof.name}.json"
    c, i = prof.capture, prof.intrinsics
    p.write_text(json.dumps({
        "profile": prof.name,
        "capture": {"size": list(c.size), "raw_size": list(c.raw_size),
                    "format": c.format, "hflip": c.hflip, "vflip": c.vflip},
        "intrinsics": {"K": i.K.tolist(), "dist": i.dist.tolist(),
                       "rms_px": i.rms_px, "n_images": i.n_images,
                       "square_mm": i.square_mm, "calibrated_utc": i.calibrated_utc},
    }, indent=2) + "\n")
    return p


def load_extrinsics(path: Path | None = None) -> Extrinsics:
    j = json.loads(Path(path or CONFIG / "camera_extrinsics.json").read_text())
    e = Extrinsics(float(j["height_mm"]), float(j["tilt_deg"]),
                   float(j["forward_mm"]), float(j["right_mm"]))
    if not 10.0 < e.height_mm < 1000.0:
        raise ValueError(f"height_mm={e.height_mm} -- extrinsics must be in mm")
    if abs(e.tilt_deg) > 80.0:
        raise ValueError(f"tilt_deg={e.tilt_deg} is measured from horizontal, not vertical")
    return e


# ------------------------------------------------------------------ validation

def _validate(name: str, cap: Capture, intr: Intrinsics, p: Path) -> None:
    if intr.K.shape != (3, 3):
        raise ValueError(f"{p.name}: K must be 3x3, got {intr.K.shape}")
    if intr.dist.size not in _ACCEPTED_DIST_LEN:
        raise ValueError(f"{p.name}: dist has {intr.dist.size} coefficients")
    if cap.raw_size[0] < cap.size[0] or cap.raw_size[1] < cap.size[1]:
        raise ValueError(f"{p.name}: raw_size {cap.raw_size} smaller than size {cap.size}")
    if cap.hflip != cap.vflip:
        raise ValueError(
            f"{p.name}: hflip={cap.hflip} vflip={cap.vflip} -- a single flip mirrors the "
            "image and makes the camera frame left-handed. Use both or neither.")

    # The check that would have caught the cropped-sensor bug: a K calibrated at a
    # different resolution puts the principal point nowhere near the frame centre.
    if intr.calibrated:
        for axis, c, n in (("cx", intr.cx, cap.width), ("cy", intr.cy, cap.height)):
            if abs(c - n / 2) > 0.15 * n:
                raise ValueError(
                    f"{p.name}: {axis}={c:.1f} is far from the centre of a {n}px axis -- "
                    f"these intrinsics were probably calibrated at another resolution")


# ------------------------------------------------------------------- singletons
# No module-level K/DIST: with two profiles a bare `K` is ambiguous, and that
# ambiguity is exactly what hid the cropped-sensor bug. Name the profile instead.

EXTRINSICS = load_extrinsics()