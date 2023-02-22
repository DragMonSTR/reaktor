const int SENSORS_PINS_NUMBER = 8;
const int SENSORS_PINS[] = {A0, A1, A2, A3, A4, A5, A6, A7};

const char MEASURE = 'm';
const char CONNECT_SENSOR = 'c';

int sensorConnectedStatus[SENSORS_PINS_NUMBER];


void setup() {
    Serial.begin(9600);
    Serial.println(SENSORS_PINS_NUMBER);
}


void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        if (command[0] == MEASURE) {
            measureConnectedSensors();
        } else {
            updateSensors(command);
        }
    }
}


void updateSensors(String connectedStatus) {
    for (int i = 0; i < SENSORS_PINS_NUMBER; i++) {
        if (connectedStatus[i] == CONNECT_SENSOR) {
            sensorConnectedStatus[i] = true;
        }
    }
}


void measureConnectedSensors() {
    String portMessage = "";
    for (int pinIndex = 0; pinIndex < SENSORS_PINS_NUMBER; pinIndex++) {
        if (sensorConnectedStatus[pinIndex]) {
            int sensorValue = getSensorValue(pinIndex);
            portMessage += String(sensorValue) + " ";
        }
    }
    Serial.println(portMessage);
}


int getSensorValue(int pinIndex) {
    int pin = SENSORS_PINS[pinIndex];
    return analogRead(pin);
}