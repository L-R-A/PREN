int uRef = 3; // Reverenzspannung für ADC in V
int uMes = 0; // Gemessener Spannungswert
int adcVal = 0; // Gemessener Wert von ADC (0-1024)

void setup() {
  Serial.begin(9600);
}

void loop() {
  adcVal = analogRead(A0);
  uMes = uRef - (uRef/1024)*adcVal;   // Berechnung des aktuellen Spannungswerts
  Serial.println(uMes);

  delay(300);
}
