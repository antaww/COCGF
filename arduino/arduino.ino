#include <Servo.h>
Servo servo;
int pos = 180;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo.write(pos);
}

void loop() {
  if (Serial.available() > 0) {
    int value = Serial.parseInt();

    if(value == 1) {
      for(pos = 150; pos >= 0; pos -= 1) {
          servo.write(pos);
          delay(5);
        }
      
        for(pos = 0; pos <= 150; pos += 1) {
          servo.write(pos);
          delay(5);
        }
    } else {
      // do nothing
    }
  }
  delay(500);
}