const int SENSORS_PINS_NUMBER = 8;
const int SENSORS_PINS[] = {A0, A1, A2, A3, A4, A5, A6, A7};

const char MEASURE = 'm';
const char CONNECT_SENSOR = 'c';
const char DISCONNECT_SENSOR = 'd';

int sensorConnectedStatus[SENSORS_PINS_NUMBER];


void setup() {
    Serial.begin(9600);
    Serial.println(SENSORS_PINS_NUMBER);
}


void loop() {
    if (Serial.available() > 0) {
        String command = readCommand();
        processCommand(command);
    }
}


String readCommand() {
    return Serial.readStringUntil('\n');
}


void processCommand(String command) {
    char commandType = getCommandType(command);
    int commandParameter = getCommandParameter(command);

    if (commandType == MEASURE) {
        measureConnectedSensors();
    }
    else if (commandType == CONNECT_SENSOR) {
        connectSensor(commandParameter);
    }
    else if (commandType == DISCONNECT_SENSOR) {
        disconnectSensor(commandParameter);
    }
    else {
        Serial.println("Unknown command");
    }
}


char getCommandType(String command) {
    return command[0];
}


int getCommandParameter(String command) {
    return command[1] - '0';
}


void connectSensor(int sensorIndex) {
    sensorConnectedStatus[sensorIndex] = true;
}


void disconnectSensor(int sensorIndex) {
    sensorConnectedStatus[sensorIndex] = false;
}


void measureConnectedSensors() {
    String portMessage = "";
    for (int pinIndex = 0; pinIndex < SENSORS_PINS_NUMBER; pinIndex++) {
        if (!sensorConnectedStatus[pinIndex]) {
            continue;
        }

        int sensorValue = getSensorValue(pinIndex);
        portMessage += String(sensorValue) + " ";
    }
    Serial.println(portMessage);
}


int getSensorValue(int pinIndex) {
    int pin = SENSORS_PINS[pinIndex];
    float value = analogRead(pin);
    return value;
}