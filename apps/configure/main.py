from configuration import Configuration
from UI import UI

def main():
    Configuration.read_configuration_from_file()
    while True:
        UI.update()


if __name__ == '__main__':
    main()
