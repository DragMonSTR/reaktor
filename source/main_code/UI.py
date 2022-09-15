from termcolor import colored

from board import Board
from helper import Helper
from timing import Timing


class UI:
    OPTIONS = [
        'Start',
        'Update boards list',
        'Connect a sensor',
        'Disconnect a sensor',
        'Rename a sensor',
        'Change measurement interval',
        'Exit program'
    ]
    WARNING_COLOR = 'red'
    SUCCESS_COLOR = 'green'
    YELLOW_COLOR = 'yellow'
    NAME_COLOR = 'cyan'
    DEFAULT_COLOR = 'white'
    dashboard_mode = False
    last_message = ''

    @staticmethod
    def update():
        Helper.clear_console()

        if not len(Board.boards_list):
            UI.show_no_boards_error()
            return

        if UI.dashboard_mode:
            UI.print_dashboard()
            UI.print_intervals()
            print(f'Press {colored("esc", UI.YELLOW_COLOR)} to stop')
            return

        UI.print_last_message()

        UI.print_dividing_line()
        UI.print_intervals()
        UI.print_boards_configuration()
        UI.print_dividing_line()
        print()

        UI.print_commands()
        selected_option = UI.ask_for_option()
        UI.process_selected_option(selected_option)

    @staticmethod
    def show_no_boards_error():
        if len(Board.boards_list) == 0:
            print(colored('No connected boards found', UI.WARNING_COLOR))
            print('Here is a solution for you:')
            print('  1. Get any Arduino board')
            print('  2. Upload our Arduino code on it')
            print('  3. Connect your Arduino with USB to this computer\n')

        ctrl_key_text = colored('ctrl', UI.YELLOW_COLOR)
        c_key_text = colored('c', UI.YELLOW_COLOR)
        enter_key_text = colored('enter', UI.YELLOW_COLOR)
        print(f'Press {ctrl_key_text} + {c_key_text} to exit')
        print(f'Press {enter_key_text} to rescan connected boards')
        input()

    @staticmethod
    def print_dividing_line():
        print('- - - - - - - - - - - - - - - - - - - - - - ')

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
        print(f'Data file updates every {data_file_update_interval}')

    @staticmethod
    def print_boards_configuration():
        if len(Board.boards_list) == 0:
            print('No connected boards found, here is a solution for you')
            print('1. Get any Arduino board')
            print('2. Upload our Arduino code on it')
            print('3. Connect your Arduino with USB')
            print('4. Use update command')
            return

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
    def print_commands():
        print('Here are available options:')
        for i, option in enumerate(UI.OPTIONS):
            option_index = colored(str(i + 1), UI.YELLOW_COLOR)
            option_first_letter = colored(option[0], UI.YELLOW_COLOR)
            option_name = option_first_letter + option[1:]
            print(f'  {option_index} - {option_name}')

    @staticmethod
    def print_dashboard():
        sensors_list = Board.get_all_connected_sensors()

        print('+--------------------------+-----------+')
        print('|          sensor          |   value   |')
        print('+--------------------------+-----------+')
        for sensor in sensors_list:
            table_row = UI.get_dashboard_row_by_sensor(sensor)
            print(table_row)
        print('+--------------------------+-----------+')

    @staticmethod
    def get_dashboard_row_by_sensor(sensor):
        sensor_name_formatted = sensor.get_name()
        if len(sensor_name_formatted) > 24:
            sensor_name_formatted = sensor_name_formatted[:21] + '...'
        sensor_name_formatted += ' ' * (24 - len(sensor_name_formatted))

        sensor_value_formatted = str(round(sensor.get_value(), 3))
        sensor_value_formatted += ' ' * (9 - len(sensor_value_formatted))

        return f'| {sensor_name_formatted} | {sensor_value_formatted} |'

    @staticmethod
    def set_last_message(message, message_color=None):
        if message_color:
            message = colored(message, message_color)
        UI.last_message = message

    @staticmethod
    def enter_dashboard_mode():
        UI.dashboard_mode = True

    @staticmethod
    def exit_dashboard_mode():
        UI.dashboard_mode = False

    @staticmethod
    def ask_for_option():
        return input('Select your option: ')

    @staticmethod
    def process_selected_option(selected_option):
        selected_option = selected_option.lower()
        # start
        if selected_option == '1' or selected_option == 's':
            UI.enter_dashboard_mode()
        # reload configuration
        elif selected_option == '2' or selected_option == 'u':
            UI.scan_connected_boards()
        # connect sensor
        elif selected_option == '3' or selected_option == 'c':
            UI.connect_sensor()
        # disconnect sensor
        elif selected_option == '4' or selected_option == 'd':
            UI.disconnect_sensor()
        # rename sensor
        elif selected_option == '5' or selected_option == 'r':
            UI.rename_sensor()
        # exit
        elif selected_option == '7' or selected_option == 'e':
            Helper.exit_program()
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
        message += colored('"', UI.DEFAULT_COLOR)
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
        Helper.clear_console()
        print('Scanning connected boards...')
        Board.update_boards_list()
