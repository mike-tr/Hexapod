import json
from pathlib import Path


def copy_values(data, data_dummy):
    for key in data_dummy:
        if isinstance(data[key], dict):
            copy_values(data[key], data_dummy[key])
        else:
            data[key] = data_dummy[key]

class Config:
    PATH = Path(__file__).parent / "config" / "hexapod.json"
    PATH_BACKUP = Path(__file__).parent / "config" / "hexapod_backup.json"
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
 


        # self.legR : list[HexLeg] = [HexLeg("RT", self, ServoConfig(18, 90, (20, 160)), ServoConfig(17, 90, (20, 160)), ServoConfig(16, -15, (0, 115)), 
        #                                    45, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL),
        #                             HexLeg("RM", self, ServoConfig(21, 90, (20, 160)), ServoConfig(20, 90, (20, 160)), ServoConfig(19, -15, (0, 115)), 
        #                                                                        0, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL),
        #                             HexLeg("RB", self, ServoConfig(27, 90, (20, 160)), ServoConfig(23, 90, (20, 160)), ServoConfig(22, -15, (0, 115)), 
        #                                                                        -45, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL)]
        # self.legL : list[HexLeg] = [
        #                             HexLeg("LT", self, ServoConfig(13, 90, (20, 160)), ServoConfig(14, 90, (20, 160)), ServoConfig(15, 0, (0, 130)), 
        #                                    135, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL),
        #                             HexLeg("LM", self, ServoConfig(10, 85, (20, 160)), ServoConfig(11, 90, (20, 160)), ServoConfig(12, -5, (0, 130)), 
        #                                                                        180, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL),
        #                             HexLeg("LB", self, ServoConfig(31, 90, (20, 160)), ServoConfig(8, 90, (20, 160)), ServoConfig(9, -10, (0, 110)), 
        #                                                                        -135, (MOUNT_POSX_45D, MOUNT_POSY_45D, MOUNT_Z_OFFSET), self.HOME_LOCAL)]

# This file, will generate a dummy json file, that stores all hexapod data, in its relative format.


    def generate_empty(self):
        print("Generating a new dummy json file, with fake data")
        data = {"COXA_LENGTH" : 0, "FEMUR_LENGTH" : 0, "TIBIA_LENGTH" : 0}
        data["HOME_POS"] = (40.0, 0.0, -45.0)
        data["HOME_RELAXED"] = (40.0, 0.0, 0)
        data["_note1"] = "rotation_bounds are servo-command degrees, applied after rotation_offset. "
        data["_note2"] = "mount position, is the position the legs sits in relative to boudy (0,0) coordinate whichever you choose it to be."
        data["LEGS"] = {}
        for leg in self.LEGS:
            data["LEGS"][leg] = { "mount_angle" : 0, "mount_position" : (0,0,0) }
            for joint in self.JOINTS:
                data["LEGS"][leg][joint] = { "id" : 0, "rotation_offset" : 90, "rotation_bounds" : (0, 180)}
        self.jsave(data, self.PATH)

def main():
    conf = Config()
    conf.generate_empty()
    conf.load_from_backup()



if __name__ == "__main__":
    main()



