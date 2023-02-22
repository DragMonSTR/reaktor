from helper import Helper
from configuration import Configuration
import time


class Timing:
    last_dashboard_update_time = 0
    last_data_file_update_time = 0

    @staticmethod
    def fix_dashboard_update():
        Timing.last_dashboard_update_time = time.time()

    @staticmethod
    def fix_data_file_update():
        Timing.last_data_file_update_time = time.time()

    @staticmethod
    def check_if_need_to_update_dashboard():
        time_passed = time.time() - Timing.last_dashboard_update_time
        return time_passed > Configuration.dashboard_update_interval

    @staticmethod
    def check_if_need_to_update_data_file():
        time_passed = time.time() - Timing.last_data_file_update_time
        return time_passed > Configuration.data_file_update_interval
