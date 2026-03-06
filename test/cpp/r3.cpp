#include <Servo.h>

const int trigPin = 11;  
const int echoPin = 10; 
const int relayPin = 8; 
const int servoPin = 18 ; 

Servo myServo;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(relayPin, OUTPUT);

  myServo.attach(servoPin);
  
  myServo.write(180);  // Initial position of the servo

  Serial.begin(9600);  // Start serial communication
}

long getDistance() {
  long sum = 0;
  for (int i = 0; i < 5; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    long distance = (duration / 2) * 0.0344;  // Calculate distance
    sum += distance;
    delay(50); 
  }
  long averageDistance = sum / 5;
  return averageDistance;
}

void loop() {
  long distance = getDistance();
  Serial.print("Distance: ");
  Serial.println(distance);

  // Notify Python that Arduino is ready for the next operation
  Serial.println("READY");  // Send "READY" message

  if (Serial.available() > 0) {
    String command = Serial.readString();
    command.trim(); 

    Serial.println(command);  // Echo received command

    if (command == "relay_on") {
      digitalWrite(relayPin, HIGH);  // Turn on relay
    } else if (command == "relay_off") {
      digitalWrite(relayPin, LOW);  // Turn off relay
    } else if (command.startsWith("move_servo")) {
      int angle = command.substring(11).toInt();  // Extract angle from command
      if (angle >= 0 && angle <= 180) { 
        myServo.write(angle);  // Move servo to desired angle
        delay(1000);  // Wait for servo to reach position
        myServo.write(180);  // Return servo to initial position
      } else {
        Serial.println("Invalid angle. Please provide a value between 0 and 180.");
      }
    }
  }

  delay(100);  // Wait for a while before the next loop iteration
}
