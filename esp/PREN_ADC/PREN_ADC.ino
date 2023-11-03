#include <ESP8266WiFi.h>
#include <time.h>
#include <LiquidCrystal.h>

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
int actualTime = 0;
int minute = 0;
int sec = 0;
float current = 0.5;
float energy = 0;

// Variabeln Startknopf
uint16_t startButton = 14;  // GPIO04 (D2)
int startButtonState = 0;  // Status ob Schalter gedürckt oder nicht
//time_t time = 0;           // Zeitwert für Messung in Sekunden

// Variabeln Stoppknopf
uint16_t stopButton = 15;
int stopButtonState = 0;

// initialize the library by associating any needed LCD interface pin
// with the MC pin number it is connected to
// TODO
const int rs = 12, en = 13, d4 = 5, d5 = 4, d6 = 0, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(9600);

  // //Connect Wifi
  // WiFi.begin(ssid, pass);

  // // while wifi not connected, print '.'
  // // after connection leave loop
  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(500);
  //   Serial.print(".");
  // }
  // Serial.print("\n Connected with IP: ");
  // Serial.println(WiFi.localIP());

  //Set up Inputs / Outputs
  pinMode(startButton, INPUT);
  pinMode(stopButton, INPUT);

  // TODO
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);

  // TODO
  // Print a message to the LCD.
  lcd.print("Ready to GO!");
}

void loop() {
  if (digitalRead(startButton)) {
    energy = 0;
    lcd.setCursor(0,0);
    lcd.print("                ");
    lcd.setCursor(0,1);
    lcd.print("                ");
    delay(300);
    startTime = millis();
    while (!digitalRead(stopButton)) {
      //if (buffer % timeStep == 0) {
      if (millis() % timeStep) {
        // ADC Spannungsmessung
        adcVal = analogRead(A0);
        uMes = uRef - ((uRef / 1024) * adcVal);  // Berechnung des aktuellen Spannungswerts
        Serial.print("ADC Value: ");
        Serial.println(adcVal);
        Serial.print("Spannung: ");
        Serial.print(uMes);
        Serial.println(" V");

        // set the cursor to column 0, line 1
        // (note: line 1 is the second row, since counting begins with 0):
        // TODO
        actualTime = (millis() - startTime) / 1000;
        minute = actualTime /60;
        sec = actualTime % 60;
        lcd.setCursor(0, 1);
        // print the number of seconds since reset:
        lcd.print("t:"+(String)minute+":"+ (sec<10? '0'+ (String)sec: (String)sec)  + " / U:" + (String)uMes + "V");
        lcd.setCursor(0,0);
        energy += uMes*current*0.5;
        lcd.print("Energie: " + (String)(energy/3600) + "Wh");
      }
    }
  }

}
