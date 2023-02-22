import os
import glob

import serial
import serial.tools.list_ports

from sensor import Sensor


class Board:
    boards = []

    @staticmethod
    def update_boards_list(boards_configuration):
        Board.boards = []
        is_windows = str(os.name).lower() == 'nt'

        if is_windows:
            ports = serial.tools.list_ports.comports()
        else:
            ports = glob.glob('/dev/tty[UA][A-Za-z]*')

        board_index = 0
        for port in ports:
            try:
                if is_windows:
                    port_name = port.name
                else:
                    port_name = port

                sensors_number = Board.read_sensors_number(port_name)

                if len(boards_configuration) > board_index:
                    configured_board = boards_configuration[board_index]
                    if configured_board.sensors_number == sensors_number:
                        Board.boards.append(configured_board)
                        continue

                board_name = f'board-{board_index + 1}'
                board_index += 1
                board = Board(board_name, sensors_number)
                Board.boards.append(board)
                for i in range(0, sensors_number):
                    sensor_name = f'{board_name}-A{i}'
                    board.sensors.append(Sensor(sensor_name))
            except (OSError, serial.SerialException):
                pass

    @staticmethod
    def read_sensors_number(port_name):
        # port should be closed
        port = serial.Serial(port_name, 9600, timeout=1)
        while True:
            if port.in_waiting:
                response = port.readline().decode('utf-8').strip('\n\r')
                port.close()
                return int(response)

    @staticmethod
    def get_all_sensors():
        sensors = []
        for board in Board.boards:
            sensors += board.sensors
        return sensors

    def __init__(self, name, sensors_number):
        self.name = name
        self.sensors_number = sensors_number
        self.sensors = []

    def get_connected_sensors_number(self):
        connected_sensors_number = 0
        for sensor in self.sensors:
            if sensor.connected_status:
                connected_sensors_number += 1
        return connected_sensors_number
