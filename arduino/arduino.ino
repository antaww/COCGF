#include <Servo.h>
Servo servo;
int pos = 0;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo.write(pos);
}

void loop() {
   if (Serial.available() > 0) {
    int value = Serial.parseInt();
    
    if(value == 1) {
      for(pos = 0; pos <= 180; pos += 1) {
        servo.write(pos);
        delay(10);
      }

      for(pos = 180; pos >= 0; pos -= 1) {
        servo.write(pos);
        delay(10);
      }
    } else {
      // do nothing
    }
  }
  delay(500);
}