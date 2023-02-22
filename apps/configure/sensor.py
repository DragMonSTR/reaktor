class Sensor:
    def __init__(self, board, pin_index, connected_status=False):
        self.board = board
        self.pin_index = pin_index
        self.name = f'{board.device_name}_pin-A{pin_index}'
        self.connected_status = connected_status
        self.value = 0

    def connect(self):
        self.connected_status = True

    def disconnect(self):
        self.connected_status = False

    def rename(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = float(new_value)

    def get_connected_status(self):
        return self.connected_status
