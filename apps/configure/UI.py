from termcolor import colored

import os
import sys

from board import Board
from timing import Timing
from activity import Activity


class UI:
    WARNING_COLOR = 'red'
    SUCCESS_COLOR = 'green'
    YELLOW_COLOR = 'yellow'
    NAME_COLOR = 'cyan'
    MENU_OPTIONS = [
        'Rescan boards',
        'Connect a sensor',
        'Disconnect a sensor',
        'Rename a sensor',
        'Intervals settings',
        'Exit program'
    ]
    INTERVALS_OPTIONS = [
        'Dashboard update interval',
        'File with data update interval',
        'Back'
    ]
    last_message = ''

    @staticmethod
    def update():
        UI.clear_console()

        current_activity = Activity.current_activity
        if current_activity == Activity.SCAN_BOARDS:
            UI.update_scan_boards_activity()
        elif current_activity == Activity.MENU:
            UI.update_menu_activity()
        elif current_activity == Activity.INTERVALS:
            UI.update_intervals_activity()

    @staticmethod
    def update_scan_boards_activity():
        UI.scan_connected_boards()
        if len(Board.boards_list):
            Activity.current_activity = Activity.MENU
            return

        UI.clear_console()
        print(colored('No connected boards found', UI.WARNING_COLOR))
        print('Here is a solution for you:')
        print('  1. Get any Arduino board')
        print('  2. Upload our Arduino code on it')
        print('  3. Connect your Arduino with USB to this computer\n')

        ctrl_key_text = colored('ctrl', UI.YELLOW_COLOR)
        c_key_text = colored('c', UI.YELLOW_COLOR)
        enter_key_text = colored('enter', UI.YELLOW_COLOR)
        print(f'Press {ctrl_key_text} + {c_key_text} to exit program')
        print(f'Press {enter_key_text} to rescan connected boards')
        input()

    @staticmethod
    def update_menu_activity():
        UI.print_last_message()

        UI.print_intervals()
        UI.print_boards_configuration()
        UI.print_dividing_line()

        UI.print_menu_options()
        selected_option = UI.ask_for_option()
        UI.process_selected_menu_option(selected_option)

    @staticmethod
    def update_intervals_activity():
        UI.print_last_message()

        UI.print_intervals()
        UI.print_dividing_line()

        UI.print_intervals_options()
        selected_interval_option = UI.ask_for_option()
        UI.process_intervals_option(selected_interval_option)

    @staticmethod
    def print_dividing_line():
        print('- - - - - - - - - - - - - - - - - - - - - - \n')

    @staticmethod
    def print_last_message():
        if not UI.last_message == '':
            print(UI.last_message + '\n')

    @staticmethod
    def print_intervals():
        dashboard_update_interval = f'{Timing.dashboard_update_interval}s'
        dashboard_update_interval = colored(dashboard_update_interval, UI.YELLOW_COLOR)
        data_file_update_interval = f'{Timing.data_file_update_interval}s'
        data_file_update_interval = colored(data_file_update_interval, UI.YELLOW_COLOR)
        print(f'Dashboard updates every {dashboard_update_interval}')
        print(f'File with data updates every {data_file_update_interval}')

    @staticmethod
    def print_boards_configuration():
        print('Connected boards:')
        for board in Board.boards_list:
            UI.print_board_info(board)
            for pin_index, sensor in enumerate(board.sensors_list):
                UI.print_sensor_info(sensor, pin_index)

    @staticmethod
    def print_board_info(board):
        board_name = colored(board.device_name, UI.NAME_COLOR)
        connected_sensors_number = board.get_connected_sensors_number()
        all_sensors_number = board.get_all_sensors_number()
        print(f'{board_name} '
              f'({connected_sensors_number}/{all_sensors_number} '
              f'sensors connected)')

    @staticmethod
    def print_sensor_info(sensor, pin_index):
        sensor_name = colored(sensor.get_name(), UI.NAME_COLOR)
        if sensor.connected_status:
            sensor_connection = f'connected to pin A{pin_index}'
        else:
            sensor_connection = f'disconnected from pin A{pin_index}'
        print(f'  {sensor_name}: {sensor_connection}')

    @staticmethod
    def print_menu_options():
        print('Here are available options:')
        UI.print_options(UI.MENU_OPTIONS)

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
    def get_dashboard_row_by_sensor(sensor):
        sensor_name_formatted = sensor.get_name()
        if len(sensor_name_formatted) > 40:
            sensor_name_formatted = sensor_name_formatted[:37] + '...'
        sensor_name_formatted += ' ' * (40 - len(sensor_name_formatted))

        sensor_value_formatted = str(round(sensor.get_value(), 3))
        sensor_value_formatted += ' ' * (9 - len(sensor_value_formatted))

        return f'| {sensor_name_formatted} | {sensor_value_formatted} |'

    @staticmethod
    def ask_for_option():
        return input('Select your option: ')

    @staticmethod
    def process_selected_menu_option(selected_option):
        selected_option = selected_option.lower()

        # reload configuration
        if selected_option == '1' or selected_option == 'r':
            Activity.current_activity = Activity.SCAN_BOARDS
            UI.last_message = ''
        # connect sensor
        elif selected_option == '2' or selected_option == 'c':
            UI.connect_sensor()
        # disconnect sensor
        elif selected_option == '3' or selected_option == 'd':
            UI.disconnect_sensor()
        # rename sensor
        elif selected_option == '4' or selected_option == 'r':
            UI.rename_sensor()
        # intervals settings
        elif selected_option == '5' or selected_option == 'i':
            Activity.current_activity = Activity.INTERVALS
        # exit
        elif selected_option == '6' or selected_option == 'e':
            UI.exit_program()
        else:
            message = colored('There is no option "', UI.WARNING_COLOR)
            message += colored(selected_option, UI.NAME_COLOR)
            message += colored('"', UI.WARNING_COLOR)
            UI.set_last_message(message)

    @staticmethod
    def connect_sensor():
        sensor_name = input('Which sensor do you want to connect:\n')

        if not Board.find_sensor_by_name(sensor_name):
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name, UI.NAME_COLOR)
            message += colored('" not found', UI.WARNING_COLOR)
            UI.set_last_message(message)
            return

        if Board.find_sensor_by_name(sensor_name).connected_status:
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name, UI.NAME_COLOR)
            message += colored('" already connected', UI.WARNING_COLOR)
            UI.set_last_message(message)

        Board.connect_sensor(sensor_name)
        message = colored('Sensor "', UI.SUCCESS_COLOR)
        message += colored(sensor_name, UI.NAME_COLOR)
        message += colored('" connected', UI.SUCCESS_COLOR)
        UI.set_last_message(message)

    @staticmethod
    def disconnect_sensor():
        sensor_name = input('Which sensor do you want to disconnect:\n')

        if not Board.find_sensor_by_name(sensor_name):
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name, UI.NAME_COLOR)
            message += colored('" not found', UI.WARNING_COLOR)
            UI.set_last_message(message)
            return

        if not Board.find_sensor_by_name(sensor_name).connected_status:
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name, UI.NAME_COLOR)
            message += colored('" already disconnected', UI.WARNING_COLOR)
            UI.set_last_message(message)

        Board.disconnect_sensor(sensor_name)
        message = colored('Sensor "', UI.SUCCESS_COLOR)
        message += colored(sensor_name, UI.NAME_COLOR)
        message += colored('" disconnected', UI.SUCCESS_COLOR)

    @staticmethod
    def rename_sensor():
        sensor_name_old = input('Which sensor do you want to rename:\n')
        sensor = Board.find_sensor_by_name(sensor_name_old)

        if not sensor:
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name_old, UI.NAME_COLOR)
            message += colored('" not found', UI.WARNING_COLOR)
            UI.set_last_message(message)
            return

        message = 'Enter new name for sensor "'
        message += colored(sensor_name_old, UI.NAME_COLOR)
        message += '"'
        sensor_name_new = input(message + '\n')

        if sensor_name_new == sensor_name_old:
            message = 'New sensor name is the same as old one'
            UI.set_last_message(message, UI.WARNING_COLOR)
            return

        if Board.find_sensor_by_name(sensor_name_new):
            message = colored('Sensor "', UI.WARNING_COLOR)
            message += colored(sensor_name_new, UI.NAME_COLOR)
            message += colored('" already exists', UI.WARNING_COLOR)
            UI.set_last_message(message)
            return

        Board.rename_sensor(sensor_name_old, sensor_name_new)
        message = colored('Sensor "', UI.SUCCESS_COLOR)
        message += colored(sensor_name_old, UI.NAME_COLOR)
        message += colored('" renamed to "', UI.SUCCESS_COLOR)
        message += colored(sensor_name_new, UI.NAME_COLOR)
        message += colored('"', UI.SUCCESS_COLOR)
        UI.set_last_message(message)

    @staticmethod
    def scan_connected_boards():
        UI.clear_console()
        print('Scanning connected boards...')
        Board.update_boards_list()

    @staticmethod
    def print_intervals_options():
        print('Here are available intervals to change:')
        UI.print_options(UI.INTERVALS_OPTIONS)

    @staticmethod
    def process_intervals_option(selected_option):
        selected_option = selected_option.lower()
        # dashboard update interval
        if selected_option == '1' or selected_option == 'd':
            UI.change_dashboard_update_interval()
        # file data update interval
        elif selected_option == '2' or selected_option == 'f':
            UI.change_data_file_update_interval()
        # back
        elif selected_option == '3' or selected_option == 'b':
            Activity.current_activity = Activity.MENU
        else:
            message = colored('There is no option "', UI.WARNING_COLOR)
            message += colored(selected_option, UI.NAME_COLOR)
            message += colored('"', UI.WARNING_COLOR)
            UI.set_last_message(message)

    @staticmethod
    def change_dashboard_update_interval():
        UI.clear_console()
        UI.print_last_message()
        UI.print_intervals()
        UI.print_dividing_line()

        question_text = 'Enter new dashboard update interval in seconds: '
        new_interval = UI.ask_for_interval(question_text)
        if not new_interval:
            return

        min_interval = Timing.MIN_DASHBOARD_UPDATE_INTERVAL
        max_interval = Timing.MAX_DASHBOARD_UPDATE_INTERVAL

        if new_interval < min_interval:
            message = colored(
                'Minimum dashboard update interval is ', UI.WARNING_COLOR)
            message += colored(min_interval, UI.YELLOW_COLOR)
            UI.set_last_message(message)
            return

        if new_interval > max_interval:
            message = colored(
                'Maximum dashboard update interval is ', UI.WARNING_COLOR)
            message += colored(max_interval, UI.YELLOW_COLOR)
            UI.set_last_message(message)
            return

        Timing.set_dashboard_update_interval(new_interval)
        UI.set_last_message('Intervals were updated', UI.SUCCESS_COLOR)

    @staticmethod
    def change_data_file_update_interval():
        UI.clear_console()
        UI.print_last_message()
        UI.print_intervals()
        UI.print_dividing_line()

        question_text = 'Enter new data file update interval in seconds: '
        new_interval = UI.ask_for_interval(question_text)
        if not new_interval:
            return

        min_interval = Timing.MIN_DATA_FILE_UPDATE_INTERVAL
        max_interval = Timing.MAX_DATA_FILE_UPDATE_INTERVAL

        if new_interval < min_interval:
            message = colored(
                'Minimum data file update interval is ', UI.WARNING_COLOR)
            message += colored(min_interval, UI.YELLOW_COLOR)
            UI.set_last_message(message)
            return

        if new_interval > max_interval:
            message = colored(
                'Maximum data file update interval is ', UI.WARNING_COLOR)
            message += colored(max_interval, UI.YELLOW_COLOR)
            UI.set_last_message(message)
            return

        Timing.set_data_file_update_interval(new_interval)
        UI.set_last_message('Intervals were updated', UI.SUCCESS_COLOR)

    @staticmethod
    def ask_for_interval(question_test):
        try:
            return int(input(question_test))
        except ValueError:
            UI.set_last_message('Interval should be a number', UI.WARNING_COLOR)
            return None

    @staticmethod
    def print_options(options):
        for i, option in enumerate(options):
            option_index = colored(str(i + 1), UI.YELLOW_COLOR)
            option_first_letter = colored(option[0], UI.YELLOW_COLOR)
            option_name = option_first_letter + option[1:]
            print(f'  {option_index} - {option_name}')

    @staticmethod
    def set_last_message(message, message_color=None):
        if message_color:
            message = colored(message, message_color)
        UI.last_message = message

    @staticmethod
    def clear_console():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def exit_program():
        sys.exit()
