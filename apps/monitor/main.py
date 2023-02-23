from configuration import Configuration
from timing import Timing
from helper import Helper
from board import Board
from sync import Sync
from UI import UI


def execute_dashboard_loop_iteration():
    Sync.update_public_data_files()

    need_to_update_dashboard = Timing.check_if_need_to_update_dashboard()
    need_to_update_data_file = Timing.check_if_need_to_update_data_file()

    if need_to_update_dashboard or need_to_update_data_file:
        Board.measure_all_boards()
        Timing.fix_dashboard_update()
        if need_to_update_data_file:
            Timing.fix_data_file_update()
            Sync.save_measurements_to_storage()
        UI.update()

    Sync.update_public_data_files()
    Sync.update_drive_files()


def main():
    try_to_create_boards()

    Sync.cloud_authenticate()

    while True:
        execute_dashboard_loop_iteration()

def try_to_create_boards():
    while True:
        try:
            Helper.clear_console()
            Configuration.read_configuration_from_file()
            Board.update_boards_list(Configuration.boards)
            if len(Board.get_all_connected_sensors()) == 0:
                raise UserWarning
            break
        except (FileNotFoundError, ValueError, IndexError):
            Configuration.reset()
            UI.print_error('Settings configuration is damaged or was not created yet')
            UI.print_configuration_guide()
            input()
        except UserWarning:
            Board.disconnect_boards()
            Configuration.reset()
            UI.print_error('No connected sensors were configured')
            UI.print_configuration_guide()
            input()


if __name__ == '__main__':
    main()
