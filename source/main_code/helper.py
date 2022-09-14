import time

from pynput.keyboard import Key, Listener
import serial.tools.list_ports
from datetime import datetime
from os import system, name
import sys


class Helper:
    key_listener = None
    last_pressed_key = None

    @staticmethod
    def exit_program():
        sys.exit()

    @staticmethod
    def clear_console():
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    @staticmethod
    def on_key_press(key):
        Helper.last_pressed_key = key
        Helper.last_pressed_key_processed = False

    @staticmethod
    def start_key_listener():
        Helper.reset_last_pressed_key()
        Helper.key_listener = Listener(on_release=Helper.on_key_press)
        Helper.key_listener.start()

    @staticmethod
    def stop_key_listener():
        Helper.reset_last_pressed_key()
        Helper.key_listener.stop()

    @staticmethod
    def reset_last_pressed_key():
        Helper.last_pressed_key = None

    @staticmethod
    def is_last_pressed_key_esc():
        return Helper.last_pressed_key == Key.esc

    @staticmethod
    def get_current_date_string():
        return datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def get_current_time_string():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_current_time():
        return time.time()
