from constants import Constants
import time

class Configuration:
    dashboard_update_interval = 0
    data_file_update_interval = 0
    boards = []

    @staticmethod
    def read_configuration_from_file():
        file = open(Constants.CONFIGURATION_FILE_PATH, 'r')
        file_lines = file.readlines()

        Configuration.dashboard_update_interval = int(file_lines[0].split(' ')[0])
        Configuration.data_file_update_interval = int(file_lines[1].split(' ')[0])

        line_index = 2
        while line_index < len(file_lines):
            board_name = file_lines[line_index].split(':')[0]
            sensors_number = int(file_lines[line_index].split(':')[1])
            board = ConfiguredBoard(board_name, sensors_number)
            Configuration.boards.append(board)
            line_index += 1
            for i in range(0, sensors_number):
                line = file_lines[line_index + i].strip()
                sensor_name = line.split(':')[0]
                sensor_connected_status = False
                if line.split(':')[1] == 'connected':
                    sensor_connected_status = True
                sensor = ConfiguredSensor(sensor_name, sensor_connected_status)
                board.sensors.append(sensor)
            line_index += sensors_number

        file.close()

    @staticmethod
    def reset():
        Configuration.dashboard_update_interval = 0
        Configuration.data_file_update_interval = 0
        Configuration.boards = []

class ConfiguredBoard:
    def __init__(self, name, sensors_number):
        self.name = name
        self.sensors_number = sensors_number
        self.sensors = []

class ConfiguredSensor:
    def __init__(self, name, connected_status):
        self.name = name
        self.connected_status = connected_status