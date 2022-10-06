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
    def make_dashboard_updated():
        interval = Timing.dashboard_update_interval
        current_time = Timing.get_current_time()

        if Timing.last_dashboard_update_time + 2 * interval > current_time:
            Timing.last_dashboard_update_time += interval
        else:
            Timing.last_dashboard_update_time = current_time

    @staticmethod
    def make_data_file_updated():
        interval = Timing.data_file_update_interval
        current_time = Timing.get_current_time()

        if Timing.last_data_file_update_time + 2 * interval > current_time:
            Timing.last_data_file_update_time += interval
        else:
            Timing.last_data_file_update_time = current_time

    @staticmethod
    def check_if_need_to_update_dashboard():
        time_passed = Timing.get_current_time() - Timing.last_dashboard_update_time
        return time_passed > Timing.dashboard_update_interval

    @staticmethod
    def check_if_need_to_update_data_file():
        time_passed = Timing.get_current_time() - Timing.last_data_file_update_time
        return time_passed > Timing.data_file_update_interval

    @staticmethod
    def get_current_time():
        return time.time()
