from helper import Helper
from timing import Timing
from board import Board
from sync import Sync
from UI import UIActivity
from UI import UI


def execute_dashboard_loop_iteration():
    print('dashboard loop iteration')
    if Helper.is_last_pressed_key_esc():
        UIActivity.open_menu_activity()
        return

    Sync.update_public_data_file()

    print('public data updated')

    need_to_update_dashboard = Timing.check_if_need_to_update_dashboard()
    need_to_update_data_file = Timing.check_if_need_to_update_data_file()

    print(need_to_update_data_file)

    if need_to_update_dashboard or need_to_update_data_file:
        Board.measure_all_boards()
        Timing.make_dashboard_updated()
        if need_to_update_data_file:
            Timing.make_data_file_updated()
            Sync.save_measurements_to_storage()
            Sync.cloud_authenticate()
            print('authenticated')
            Sync.upload_program_data_to_cloud()
        UI.update()


def main():
    Sync.cloud_authenticate()
    Helper.start_key_listener()

    while True:
        if UIActivity.get_current_activity() == UIActivity.DASHBOARD_ACTIVITY:
            execute_dashboard_loop_iteration()
        else:
            UI.update()


if __name__ == '__main__':
    main()
