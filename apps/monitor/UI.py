from termcolor import colored

from board import Board
from helper import Helper
from configuration import Configuration


class UI:
    YELLOW_COLOR = 'yellow'

    @staticmethod
    def update():
        Helper.clear_console()
        UI.print_dashboard()
        UI.print_intervals()

    @staticmethod
    def print_dashboard():
        sensors_list = Board.get_all_connected_sensors()
        print('+------------------------------------------+-----------+')
        print('|                sensor name               |   value   |')
        print('+------------------------------------------+-----------+')
        for sensor in sensors_list:
            table_row = UI.get_dashboard_row_by_sensor(sensor)
            print(table_row)
        print('+------------------------------------------+-----------+')

    @staticmethod
    def print_intervals():
        dashboard_update_interval = colored(
            f'{Configuration.dashboard_update_interval}s', 'yellow')
        print(f'Dashboard updates every {dashboard_update_interval}')

        data_file_update_interval = colored(
            f'{Configuration.data_file_update_interval}s', 'yellow')
        print(f'File with data updates every {data_file_update_interval}')

    @staticmethod
    def get_dashboard_row_by_sensor(sensor):
        name_length = 40
        name = sensor.name.ljust(name_length)
        if len(name) > name_length:
            name = name[:name_length - 3] + '...'

        value_length = 9
        value = str(round(sensor.value, 3)).ljust(value_length)

        return f'| {name} | {value} |'
