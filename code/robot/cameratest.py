"""Report what the sensor is ACTUALLY doing for each raw-mode request.
Run on the Pi:  python3 fov_probe.py
Saves one frame per config so you can compare, and prints the numbers that matter.
"""
import time
from picamera2 import Picamera2

MAIN = (1280, 720)
RAW_OPTIONS = [None, (1536, 864), (2304, 1296), (4608, 2592)]

picam2 = Picamera2()
props = picam2.camera_properties
print("camera_properties:")
for k in ("Model", "PixelArraySize", "PixelArrayActiveAreas", "ScalerCropMaximum"):
    if k in props:
        print(f"  {k:<22} {props[k]}")
print("\nsensor_modes:")
for m in picam2.sensor_modes:
    print(f"  size={m.get('size')}  crop_limits={m.get('crop_limits')}  "
          f"fps={m.get('fps')}  bit_depth={m.get('bit_depth')}")
print()

hdr = f"{'raw requested':>16} | {'raw applied':>13} | {'ScalerCrop':>26} | {'% of array':>10}"
print(hdr)
print("-" * len(hdr))

arr_w, arr_h = props.get("PixelArraySize", (4608, 2592))

for raw in RAW_OPTIONS:
    kw = {"main": {"size": MAIN, "format": "RGB888"}}
    if raw is not None:
        kw["raw"] = {"size": raw}
    cfg = picam2.create_video_configuration(**kw)
    picam2.configure(cfg)
    picam2.start()
    time.sleep(0.6)                                  # let AE/AWB settle a little
    md = picam2.capture_metadata()
    applied = picam2.camera_configuration().get("raw", {}).get("size")
    sc = md.get("ScalerCrop")
    pct = f"{100.0 * sc[2] / arr_w:.0f} x {100.0 * sc[3] / arr_h:.0f}" if sc else "?"
    name = f"raw_{raw[0]}x{raw[1]}" if raw else "raw_default"
    picam2.capture_file(f"{name}.jpg")
    picam2.stop()
    print(f"{str(raw):>16} | {str(applied):>13} | {str(sc):>26} | {pct:>10}")

picam2.close()
print("\nIf ScalerCrop is identical across rows, field of view is identical and")
print("the mode listing's 'crop' is not what I thought. Compare the saved jpgs.")