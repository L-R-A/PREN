void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("ADC Value: ");
  Serial.println(analogRead(A0));
  delay(300);
}
