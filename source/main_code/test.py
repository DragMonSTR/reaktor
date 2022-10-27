import constant

with open(constant.SETTINGS_FILE_PATH) as settings_file:
    lines = settings_file.readlines()
settings_file.close()

for line in lines:
    sensor_name = line.split(';')[0]
    connected_status = line.split(';')[1]
    print(sensor_name)
    print(connected_status)
