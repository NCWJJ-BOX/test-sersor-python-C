#include <Servo.h>  // นำเข้าไลบรารี Servo

#define trigPin 10  // กำหนดขา trig
#define echoPin 9   // กำหนดขา echo
#define servoPin 6  // กำหนดขา Servo

Servo myServo;  // สร้างอ็อบเจกต์ของเซอร์โว

void setup() {
  Serial.begin(9600);  // เริ่มต้นการสื่อสารกับ Raspberry Pi
  pinMode(trigPin, OUTPUT);  // ตั้งค่า trig เป็น OUTPUT
  pinMode(echoPin, INPUT);  // ตั้งค่า echo เป็น INPUT
  myServo.attach(servoPin);  // เชื่อมต่อเซอร์โวเข้ากับขา servoPin
}

void loop() {
  // สร้าง pulse บน trigPin เพื่อเริ่มการวัด
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // วัดระยะเวลาที่ echoPin รับเสียงสะท้อนกลับ
  long duration = pulseIn(echoPin, HIGH);

  // คำนวณระยะทางจากเวลา (คำนวณจากความเร็วเสียง)
  long distance = duration * 0.0344 / 2;  // ความเร็วเสียงประมาณ 343 m/s หรือ 0.0344 cm/μs

  // // ส่งระยะทางผ่าน Serial
  // Serial.println(distance);

  // เช็คว่า ระยะทางน้อยกว่า 20 ซม. หรือไม่
  if (distance < 20) {
    Serial.println(1);  // ส่งคำสั่ง Capture ไปที่ Raspberry Pi
    delay(1000);
    myServo.write(90);  // หมุนเซอร์โวไปที่ 90 องศา (เปิด)
  } else {
    Serial.println(0);
    delay(1000);
    myServo.write(0); 
      // ส่งคำสั่ง Capture ไปที่ Raspberry Pi
      // หมุนเซอร์โวไปที่ 0 องศา (ปิด)
    // Serial.println("Servo OFF");
  }

  delay(100);  // หน่วงเวลาเพื่อไม่ให้ข้อมูลส่งบ่อยเกินไป
}
