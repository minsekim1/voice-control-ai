int led = 8; // GPIO 2 핀 사용

void setup() {
  pinMode(led, OUTPUT);
}

void loop() {
  digitalWrite(led, HIGH); // turn on the LED
  delay(700);
  digitalWrite(led, LOW); // turn off the LED
  delay(700);
  digitalWrite(led, HIGH); // turn on the LED
  delay(500);
  digitalWrite(led, LOW); // turn off the LED
  delay(500);
}
