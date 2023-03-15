#include <Servo.h>
Servo myservo;

int angle = 0;
void setup() {
  Serial.begin(115200);
  myservo.attach(9);
}
void loop() {
  if (Serial.available() > 0) {
    angle = Serial.readString().toInt();
    Serial.print("You sent me: ");
    Serial.println(angle);
    
    myservo.write(angle);             
    delay(15); 
  }
}
