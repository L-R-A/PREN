#include <ESP8266WiFi.h>
#include <time.h>

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "Hadouken";
char pass[] = "Humhomburarum42";

// Variabeln Messungen
float uRef = 3.3;    // Reverenzspannung für ADC in V
float uMes = 0.0;    // Gemessener Spannungswert
float adcVal = 0;    // Gemessener Wert von ADC (0-1024)
int timeStep = 500;  // Time Step zwischen den einzelnen Messpunkten
int startTime = millis();

// Variabeln Startknopf
uint16_t startButton = 4;  // GPIO04 (D2)
int startButtonState = 0;  // Status ob Schalter gedürckt oder nicht
//time_t time = 0;           // Zeitwert für Messung in Sekunden

// time_t setupTime() {
//   configTime(5 * 3600, 0, "pool.ntp.org");
//   while (!time(nullptr)) {
//     Serial.println("*");
//     delay(500);
//   }
// }

void setup() {
  Serial.begin(9600);

  //Connect Wifi
  WiFi.begin(ssid, pass);

  // while wifi not connected, print '.'
  // after connection leave loop
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\n Connected with IP: ");
  Serial.println(WiFi.localIP());

  // Start Time Function
  //setupTime();

  //Set up Inputs / Outputs
  pinMode(startButton, INPUT);
}

void loop() {
  // // Zeitcounter beginnen
  // time_t rawtime;
  // struct tm* timeinfo;
  // time(&rawtime);
  // timeinfo = localtime(&rawtime);
  // char buffer[80];
  // strftime(buffer, 80, "%Y%m%d", timeinfo);
  // Serial.println(buffer);


  startButtonState = digitalRead(startButton);
  if (!startButtonState) {
    while (!startButtonState) {
      //if (buffer % timeStep == 0) {
      if (millis() % 500) {
        // ADC Spannungsmessung
        adcVal = analogRead(A0);
        uMes = uRef - ((uRef / 1024) * adcVal);  // Berechnung des aktuellen Spannungswerts
        Serial.print("ADC Value: ");
        Serial.println(adcVal);
        Serial.print("Spannung: ");
        Serial.print(uMes);
        Serial.println(" V");
      }
    }
  }

  delay(500);
}
