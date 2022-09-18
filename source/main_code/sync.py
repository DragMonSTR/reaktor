import shutil

from exel import Excel
from board import Board
import constant


class Sync:
    @staticmethod
    def upload_measurements_to_file():
        Sync.upload_measurements_to_working_file()
        Sync.copy_working_file_to_public()

    @staticmethod
    def upload_measurements_to_working_file():
        connected_sensors = Board.get_all_connected_sensors()
        Excel.open(constant.WORKING_FILE_PATH)
        Excel.add_measurements(connected_sensors)
        Excel.save(constant.WORKING_FILE_PATH)

    @staticmethod
    def copy_working_file_to_public():
        try:
            shutil.copyfile(constant.WORKING_FILE_PATH, constant.PUBLIC_FILE_PATH)
        except:
            return
