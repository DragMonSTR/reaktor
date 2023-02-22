class Configuration:
    dashboard_update_interval = 5
    data_file_update_interval = 15
    sensor_names = []
    sensor_connected_statuses = []
    FILE_PATH = '../../data/configuration.txt'

    @staticmethod
    def read_configuration_from_file():
        try:
            file = open(Configuration.FILE_PATH, 'r')
            file_lines = file.readlines()
            Configuration.dashboard_update_interval = int(file_lines[0].split(' ')[0])
            Configuration.data_file_update_interval = int(file_lines[1].split(' ')[0])
            file.close()
        except FileNotFoundError:
            Configuration.write_configuration_to_file()
        except ValueError:
            Configuration.write_configuration_to_file()

    @staticmethod
    def write_configuration_to_file():
        file = open(Configuration.FILE_PATH, 'w')

        file.write(str(Configuration.dashboard_update_interval))
        file.write(' - dashboard update interval\n')

        file.write(str(Configuration.data_file_update_interval))
        file.write(' - data file update interval\n')

        for i in range(len(Configuration.sensor_names)):
            file.write(Configuration.sensor_names[i])
            if Configuration.sensor_connected_statuses[i]:
                file.write(':connected\n')
            else:
                file.write(':disconnected\n')

        file.close()

Configuration.read_configuration_from_file()