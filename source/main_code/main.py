from helper import Helper
from memory import Memory
from board import Board
from sync import Sync
from UI import UI


def execute_dashboard_loop_iteration():
    if Helper.is_last_pressed_key_esc():
        UI.exit_dashboard_mode()
        return

    need_to_update_dashboard = Memory.check_if_need_to_update_dashboard()
    need_to_update_data_file = Memory.check_if_need_to_update_data_file()

    if need_to_update_dashboard or need_to_update_data_file:
        Board.measure_all_boards()
        current_time = Helper.get_current_time()
        Memory.set_last_dashboard_update_time(current_time)
        if need_to_update_data_file:
            Memory.set_data_file_update_time(current_time)
            Sync.upload_measurements_to_file()
        UI.update()


def main():
    Helper.start_key_listener()
    while True:
        if not Board.boards_list:
            UI.scan_connected_boards()

        if not UI.dashboard_mode:
            UI.update()
            continue

        execute_dashboard_loop_iteration()


if __name__ == '__main__':
    main()
