from termcolor import colored

import os
import sys

from board import Board
from activity import Activity
from constants import Constants
from configuration import Configuration


class UI:
    WARNING_COLOR = 'red'
    SUCCESS_COLOR = 'green'
    YELLOW_COLOR = 'yellow'
    NAME_COLOR = 'cyan'
    MENU_OPTIONS = [
        'Update connected boards',
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
        print('Scanning connected boards...')
        Board.update_boards_list(Configuration.boards)
        if len(Board.boards):
            Configuration.set_boards(Board.boards)
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
        if UI.last_message == '':
            print('\n')
            return

        print(UI.last_message + '\n')

    @staticmethod
    def print_intervals():
        dashboard_update_interval = f'{Configuration.dashboard_update_interval}s'
        dashboard_update_interval = colored(dashboard_update_interval, UI.YELLOW_COLOR)
        data_file_update_interval = f'{Configuration.data_file_update_interval}s'
        data_file_update_interval = colored(data_file_update_interval, UI.YELLOW_COLOR)
        print(f'Dashboard updates every {dashboard_update_interval}')
        print(f'File with data updates every {data_file_update_interval}')

    @staticmethod
    def print_boards_configuration():
        print('Found boards and sensors:')
        sensor_index = 1
        for board in Board.boards:
            name = colored(board.name, UI.NAME_COLOR)
            sensors_number = board.sensors_number
            connected_sensors_number = board.get_connected_sensors_number()
            sensors_message = f'{connected_sensors_number}/{sensors_number}'
            print(name, sensors_message, 'sensors connected')
            for pin_index, sensor in enumerate(board.sensors):
                UI.print_sensor_info(sensor_index, sensor, pin_index)
                sensor_index += 1

    @staticmethod
    def print_sensor_info(sensor_index, sensor, pin_index):
        sensor_index = colored(str(sensor_index).rjust(2), UI.YELLOW_COLOR)
        sensor_name = colored(sensor.name.ljust(11), UI.NAME_COLOR)
        if sensor.connected_status:
            sensor_connected = f'connected to pin A{pin_index}'
        else:
            sensor_connected = f'disconnected from pin A{pin_index}'
        print(sensor_index, sensor_name, sensor_connected)

    @staticmethod
    def print_menu_options():
        print('Here are available options:')
        UI.print_options(UI.MENU_OPTIONS)

    @staticmethod
    def ask_for_option():
        return input('Select your option: ')

    @staticmethod
    def process_selected_menu_option(selected_option):
        selected_option = selected_option.lower()

        # reload configuration
        if selected_option == '1' or selected_option == 'u':
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
        try:
            user_input = input('Enter the index of the sensor you want to connect: ')
            sensor_index = int(user_input) - 1
            if sensor_index < 0:
                raise ValueError
            sensor = Board.get_all_sensors()[sensor_index]
            if sensor.connected_status:
                raise NameError
            sensor.connected_status = True
            message = colored('Sensor ', UI.SUCCESS_COLOR)
            message += colored(sensor.name, UI.NAME_COLOR)
            message += colored(' was connected', UI.SUCCESS_COLOR)
            UI.set_last_message(message)
            Configuration.write_configuration_to_file()
        except (ValueError, IndexError):
            message = 'Sensor index should be a number between 1 and '
            message += str(len(Board.get_all_sensors()))
            UI.set_last_message(colored(message, UI.WARNING_COLOR))
        except NameError:
            message = 'You are trying to connect a sensor that is already connected'
            UI.set_last_message(colored(message, UI.WARNING_COLOR))

    @staticmethod
    def disconnect_sensor():
        try:
            user_input = input('Enter the index of the sensor you want to disconnect: ')
            sensor_index = int(user_input) - 1
            if sensor_index < 0:
                raise ValueError
            sensor = Board.get_all_sensors()[sensor_index]
            if not sensor.connected_status:
                raise NameError
            sensor.connected_status = False
            message = colored('Sensor ', UI.SUCCESS_COLOR)
            message += colored(sensor.name, UI.NAME_COLOR)
            message += colored(' was disconnected', UI.SUCCESS_COLOR)
            UI.set_last_message(message)
            Configuration.write_configuration_to_file()
        except (ValueError, IndexError):
            message = 'Sensor index should be a number between 1 and '
            message += str(len(Board.get_all_sensors()))
            UI.set_last_message(colored(message, UI.WARNING_COLOR))
        except NameError:
            message = 'You are trying to disconnect a sensor that is not connected'
            UI.set_last_message(colored(message, UI.WARNING_COLOR))

    @staticmethod
    def rename_sensor():
        try:
            user_input = input('Enter the index of the sensor you want to rename: ')
            sensor_index = int(user_input) - 1
            if sensor_index < 0:
                raise ValueError
            sensor = Board.get_all_sensors()[sensor_index]

            message = 'Enter new name for sensor '
            message += colored(sensor.name, UI.NAME_COLOR)
            message += ': '
            new_name = input(message)
            old_name = sensor.name
            if old_name == new_name:
                raise NameError

            sensor.name = new_name
            message = colored('Sensor ', UI.SUCCESS_COLOR)
            message += colored(old_name, UI.NAME_COLOR)
            message += colored(' was renamed to ', UI.SUCCESS_COLOR)
            message += colored(new_name, UI.NAME_COLOR)
            UI.set_last_message(message)
            Configuration.write_configuration_to_file()
        except (ValueError, IndexError):
            message = 'Sensor index should be a number between 1 and '
            message += str(len(Board.get_all_sensors()))
            UI.set_last_message(colored(message, UI.WARNING_COLOR))
        except NameError:
            message = 'You are trying to name a sensor with the same name'
            UI.set_last_message(colored(message, UI.WARNING_COLOR))

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

        min_interval = Constants.MIN_DASHBOARD_UPDATE_INTERVAL
        max_interval = Constants.MAX_DASHBOARD_UPDATE_INTERVAL

        try:
            interval = int(input('Enter new dashboard update interval in seconds: '))
            if interval < min_interval or interval > max_interval:
                raise ValueError
            Configuration.set_dashboard_update_interval(interval)
            message = f'Dashboard update interval was set to {interval}'
            UI.set_last_message(message, UI.SUCCESS_COLOR)
        except ValueError:
            message = f'Interval should be a number between {min_interval} and {max_interval}'
            UI.set_last_message(message, UI.WARNING_COLOR)

    @staticmethod
    def change_data_file_update_interval():
        UI.clear_console()
        UI.print_last_message()
        UI.print_intervals()
        UI.print_dividing_line()

        min_interval = Constants.MIN_DATA_FILE_UPDATE_INTERVAL
        max_interval = Constants.MAX_DATA_FILE_UPDATE_INTERVAL

        try:
            interval = int(input('Enter new data file update interval in seconds: '))
            if interval < min_interval or interval > max_interval:
                raise ValueError
            Configuration.set_data_file_update_interval(interval)
            message = f'Data file update interval was set to {interval}'
            UI.set_last_message(message, UI.SUCCESS_COLOR)
        except ValueError:
            message = f'Data file should be a number between {min_interval} and {max_interval}'
            UI.set_last_message(message, UI.WARNING_COLOR)

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
