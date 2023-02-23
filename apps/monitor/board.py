import os
import glob
import time

import serial
import serial.tools.list_ports

from sensor import Sensor


class Board:
    MEASURE = "m"
    CONNECT_SENSOR = "c"
    DISCONNECT_SENSOR = "d"

    MAX_VOLTAGE = 5
    MAX_SENSOR_VALUE = 1024
    RESISTOR_RESISTANCE = 1000

    boards = []

    @staticmethod
    def update_boards_list(configured_boards):
        Board.disconnect_boards()
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
                if len(configured_boards) < board_index:
                    raise LookupError

                configured_board = configured_boards[board_index]
                if len(configured_board.sensors) != sensors_number:
                    raise LookupError

                board = Board(port_name, configured_board)
                Board.boards.append(board)
                board_index += 1
            except (OSError, serial.SerialException):
                pass

    @staticmethod
    def read_sensors_number(port_name):
        # port should be closed
        port = serial.Serial(port_name)
        while True:
            if port.in_waiting:
                response = port.readline().decode('utf-8').strip('\n\r')
                port.close()
                return int(response)

    @staticmethod
    def disconnect_boards():
        for board in Board.boards:
            board.port.close()
        Board.boards = []

    @staticmethod
    def get_all_connected_sensors():
        sensors = []
        for board in Board.boards:
            sensors += board.get_connected_sensors()
        return sensors

    @staticmethod
    def measure_all_boards():
        for board in Board.boards:
            board.measure()

    @staticmethod
    def get_temperature_by_pin_value(sensor_value):
        sensor_voltage =\
            Board.MAX_VOLTAGE * sensor_value / Board.MAX_SENSOR_VALUE
        sensor_resistance =\
            Board.RESISTOR_RESISTANCE * sensor_voltage /\
            (Board.MAX_VOLTAGE - sensor_voltage)
        return 100 / 385 * sensor_resistance - 100000 / 385

    def __init__(self,  port_name, configured_board):
        self.name = configured_board.name
        self.port = serial.Serial(port_name)
        self.read_line()
        self.sensors = []
        connect_sensors_command = ''
        for i, configured_sensor in enumerate(configured_board.sensors):
            sensor = Sensor(self, i,
                            configured_sensor.name,
                            configured_sensor.connected_status)
            self.sensors.append(sensor)
            if sensor.connected_status:
                connect_sensors_command += 'c'
            else:
                connect_sensors_command += ' '
        self.write_line(connect_sensors_command)

    def get_all_sensors_number(self):
        return len(self.sensors)

    def get_connected_sensors_number(self):
        connected_sensors_number = 0
        for sensor in self.sensors:
            if sensor.connected_status:
                connected_sensors_number += 1
        return connected_sensors_number

    def get_connected_sensors(self):
        sensors = []
        for sensor in self.sensors:
            if sensor.connected_status:
                sensors.append(sensor)
        return sensors

    def measure(self):
        self.write_line(Board.MEASURE)
        response = self.read_line()
        connected_pins_values = response.split(' ')

        for i, sensor in enumerate(self.get_connected_sensors()):
            try:
                pin_value = int(connected_pins_values[i])
            except (ValueError, IndexError):
                pin_value = 0
            temperature = Board.get_temperature_by_pin_value(pin_value)
            sensor.set_value(temperature)

    def write_line(self, data):
        self.port.write(data.encode())

    def read_line(self):
        time_start = time.time()
        while True:
            if time.time() - time_start > 2:
                return ''
            if self.port.in_waiting:
                response = self.port.readline()
                return response.decode('utf-8').strip('\n\r')
