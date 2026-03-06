#include <Servo.h>

#define trigPin 12
#define echoPin 13
#define servoPin 18
#define infraredPin 8


Servo myServo;

void setup() {
  Serial.begin(115200);
  pinMode(infraredPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myServo.attach(servoPin);
  myServo.write(90);

  while (!Serial) { ; }  
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.0344 / 2;
  
  // Return -1 for invalid readings
  if (duration == 0 || distance > 400) return -1; 
  return distance;
}

void loop() {
  long distance = getDistance();
  int sensorValue = digitalRead(infraredPin); 
  // myServo.write(90);
  // Serial.println(distance);

  if (sensorValue == HIGH) {
    Serial.println("0"); 
  } else {
    Serial.println("2");
  }


  if (distance < 27.5) {
    Serial.println("1");
    myServo.write(0);
  } else {
      Serial.println("0");
      myServo.write(90);
  }

  delay(100);
}