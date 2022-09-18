from helper import Helper
from timing import Timing
from board import Board
from sync import Sync
from UI import UIActivity
from UI import UI


def execute_dashboard_loop_iteration():
    if Helper.is_last_pressed_key_esc():
        UIActivity.open_menu_activity()
        return

    need_to_update_dashboard = Timing.check_if_need_to_update_dashboard()
    need_to_update_data_file = Timing.check_if_need_to_update_data_file()

    if need_to_update_dashboard or need_to_update_data_file:
        Board.measure_all_boards()
        current_time = Helper.get_current_time()
        Timing.set_last_dashboard_update_time(current_time)
        if need_to_update_data_file:
            Timing.set_last_data_file_update_time(current_time)
            Sync.upload_measurements_to_file()
        UI.update()


def main():
    Helper.start_key_listener()

    while True:
        if UIActivity.get_current_activity() == UIActivity.DASHBOARD_ACTIVITY:
            execute_dashboard_loop_iteration()
        else:
            UI.update()


if __name__ == '__main__':
    main()
