from configuration import Configuration
from timing import Timing
from board import Board
from sync import Sync
from UI import UI


def execute_dashboard_loop_iteration():
    Sync.update_public_data_file()

    need_to_update_dashboard = Timing.check_if_need_to_update_dashboard()
    need_to_update_data_file = Timing.check_if_need_to_update_data_file()

    if need_to_update_dashboard or need_to_update_data_file:
        Board.measure_all_boards()
        Timing.fix_dashboard_update()
        if need_to_update_data_file:
            Timing.fix_data_file_update()
            Sync.save_measurements_to_storage()
            try:
                Sync.cloud_authenticate()
                Sync.upload_program_data_to_cloud()
            except:
                pass
        UI.update()


def main():
    Sync.cloud_authenticate()
    Configuration.read_configuration_from_file()
    Board.update_boards_list(Configuration.boards)

    while True:
        execute_dashboard_loop_iteration()


if __name__ == '__main__':
    main()
