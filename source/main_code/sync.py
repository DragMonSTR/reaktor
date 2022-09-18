import shutil

from exel import Excel
from board import Board
import constant


class Sync:
    public_file_is_up_to_date = True

    @staticmethod
    def save_measurements_to_storage():
        connected_sensors = Board.get_all_connected_sensors()
        Excel.open(constant.WORKING_FILE_PATH)
        Excel.add_measurements(connected_sensors)
        Excel.save(constant.WORKING_FILE_PATH)
        Sync.public_file_is_up_to_date = False

    @staticmethod
    def update_public_data_file():
        if Sync.public_file_is_up_to_date:
            return

        try:
            shutil.copyfile(constant.WORKING_FILE_PATH, constant.PUBLIC_FILE_PATH)
            Sync.public_file_is_up_to_date = True
        except:
            return
