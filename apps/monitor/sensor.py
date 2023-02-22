class Sensor:
    def __init__(self, board, pin_index, name, connected_status=False):
        self.board = board
        self.pin_index = pin_index
        self.name = name
        self.connected_status = connected_status
        self.value = 0

    def set_value(self, new_value):
        self.value = float(new_value)
