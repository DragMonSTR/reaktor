from helper import Helper


class Memory:
    dashboard_update_interval = 5
    data_file_update_interval = 15

    last_dashboard_update_time = 0
    last_data_file_update_time = 0

    @staticmethod
    def set_last_dashboard_update_time(new_time):
        Memory.last_dashboard_update_time = new_time

    @staticmethod
    def set_data_file_update_time(new_time):
        Memory.last_data_file_update_time = new_time

    @staticmethod
    def check_if_need_to_update_dashboard():
        current_time = Helper.get_current_time()
        time_passed = current_time - Memory.last_dashboard_update_time
        return time_passed > Memory.dashboard_update_interval

    @staticmethod
    def check_if_need_to_update_data_file():
        current_time = Helper.get_current_time()
        time_passed = current_time - Memory.last_data_file_update_time
        return time_passed > Memory.data_file_update_interval
