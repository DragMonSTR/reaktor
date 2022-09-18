from helper import Helper
import time


class Timing:
    MIN_DASHBOARD_UPDATE_INTERVAL = 3
    MAX_DASHBOARD_UPDATE_INTERVAL = 86400  # 1 day
    MIN_DATA_FILE_UPDATE_INTERVAL = 3
    MAX_DATA_FILE_UPDATE_INTERVAL = 604800  # 1 week

    dashboard_update_interval = 5
    data_file_update_interval = 15

    last_dashboard_update_time = 0
    last_data_file_update_time = 0

    @staticmethod
    def set_dashboard_update_interval(new_interval):
        Timing.dashboard_update_interval = new_interval
        if new_interval > Timing.data_file_update_interval:
            Timing.set_data_file_update_interval(new_interval)

    @staticmethod
    def set_data_file_update_interval(new_interval):
        Timing.data_file_update_interval = new_interval
        if new_interval < Timing.dashboard_update_interval:
            Timing.set_dashboard_update_interval(new_interval)

    @staticmethod
    def set_last_dashboard_update_time(new_time):
        Timing.last_dashboard_update_time = new_time

    @staticmethod
    def set_last_data_file_update_time(new_time):
        Timing.last_data_file_update_time = new_time

    @staticmethod
    def check_if_need_to_update_dashboard():
        current_time = Helper.get_current_time()
        time_passed = current_time - Timing.last_dashboard_update_time
        return time_passed > Timing.dashboard_update_interval

    @staticmethod
    def check_if_need_to_update_data_file():
        current_time = Helper.get_current_time()
        time_passed = current_time - Timing.last_data_file_update_time
        return time_passed > Timing.data_file_update_interval
