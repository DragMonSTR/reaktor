from constants import Constants
from sensor import Sensor
from board import Board

class Configuration:
    dashboard_update_interval = 5
    data_file_update_interval = 15
    boards = []

    @staticmethod
    def read_configuration_from_file():
        try:
            file = open(Constants.CONFIGURATION_FILE_PATH, 'r')
            file_lines = file.readlines()

            Configuration.dashboard_update_interval = int(file_lines[0].split(' ')[0])
            Configuration.data_file_update_interval = int(file_lines[1].split(' ')[0])

            line_index = 2
            while line_index < len(file_lines):
                board_name = file_lines[line_index].split(':')[0]
                sensors_number = int(file_lines[line_index].split(':')[1])
                board = Board(board_name, sensors_number)
                line_index += 1
                for i in range(0, sensors_number):
                    line = file_lines[line_index + i]
                    sensor_name = line.split(':')[0]
                    sensor_connected_status = False
                    if line.split(':')[1] == 'connected':
                        sensor_connected_status = True
                    sensor = Sensor(sensor_name, sensor_connected_status)
                    board.sensors.append(sensor)
                    Configuration.boards.append(board)
                line_index += sensors_number

            file.close()
        except (FileNotFoundError, ValueError):
            Configuration.write_configuration_to_file()

    @staticmethod
    def write_configuration_to_file():
        file = open(Constants.CONFIGURATION_FILE_PATH, 'w')

        file.write(str(Configuration.dashboard_update_interval))
        file.write(' - dashboard update interval\n')

        file.write(str(Configuration.data_file_update_interval))
        file.write(' - data file update interval\n')

        for board in Configuration.boards:
            file.write(f'{board.name}:{len(board.sensors)}\n')
            for sensor in board.sensors:
                file.write(sensor.name)
                if sensor.connected_status:
                    file.write(':connected\n')
                else:
                    file.write(':disconnected\n')

        file.close()

    @staticmethod
    def set_dashboard_update_interval(interval):
        Configuration.dashboard_update_interval = interval
        if interval > Configuration.data_file_update_interval:
            Configuration.data_file_update_interval = interval
        Configuration.write_configuration_to_file()

    @staticmethod
    def set_data_file_update_interval(interval):
        Configuration.data_file_update_interval = interval
        if interval < Configuration.dashboard_update_interval:
            Configuration.dashboard_update_interval = interval
        Configuration.write_configuration_to_file()

    @staticmethod
    def set_boards(boards):
        Configuration.boards = boards
        Configuration.write_configuration_to_file()