import os
import glob

class DataManager:
    @classmethod
    def dropfile(cls, pattarn: str) -> None:
        file_list = glob.glob(f"*.{pattarn}")
        for file in file_list:
            print("remove：{0}".format(file))
            os.remove(file)