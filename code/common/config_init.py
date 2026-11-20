import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.paths import CONFIG

import json


def copy_values(data, data_dummy):
    for key in data_dummy:
        if isinstance(data[key], dict):
            copy_values(data[key], data_dummy[key])
        else:
            data[key] = data_dummy[key]

class Config:
    PATH = CONFIG / "hexapod.json"
    PATH_BACKUP = CONFIG / "hexapod_backup.json"
    LEGS = ["RF", "RM", "RB", "LF", "LM", "LB"]
    JOINTS = ["COXA", "FEMUR", "TIBIA"]

    def load(self):
        self.data = json.loads(Path(self.PATH).read_text())


    def jsave(self, data, path):
        Path(path).write_text(json.dumps(data, indent=2))
    
    
    def jload(self, path):
        return json.loads(Path(path).read_text())

    def load_from_backup(self):
        data = self.jload(self.PATH)
        data_dummy = self.jload(self.PATH_BACKUP)
        copy_values(data, data_dummy)
        self.jsave(data, self.PATH)
 

    def generate_empty(self):
        print("Generating a new dummy json file, with fake data")
        data = {"COXA_LENGTH" : 0, "FEMUR_LENGTH" : 0, "TIBIA_LENGTH" : 0, "TIBIA_CURVE" : 0, "POSITION_SCALE" : 100}
        data["HOME_POS_NORM"] = (40.0, 0.0, -45.0)
        data["HOME_RELAXED_NORM"] = (40.0, 0.0, 0)
        data["_note1"] = "rotation_bounds are servo-command degrees, applied after rotation_offset. "
        data["_note2"] = "mount position, is the position the legs sits in relative to boudy (0,0) coordinate whichever you choose it to be."
        data["LEGS"] = {}
        for leg in self.LEGS:
            data["LEGS"][leg] = { "mount_angle" : 0, "mount_position" : (0,0,0) }
            for joint in self.JOINTS:
                data["LEGS"][leg][joint] = { "id" : 0, "sign" : 1, "rotation_offset" : 90, "rotation_bounds" : (0, 180)}
        self.jsave(data, self.PATH)

def main():
    conf = Config()
    conf.generate_empty()
    conf.load_from_backup()



if __name__ == "__main__":
    main()



