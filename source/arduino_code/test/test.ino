void setup() {
    Serial.begin(9600);
}

void loop() {
    String message = "mt";
    char parameter = message[1];
    int parameterInt = String(parameter).toInt();

    Serial.println(parameterInt);
    delay(1000);
}