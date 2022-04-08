#include <Servo.h>
#include "Wire.h"

// Left Engine
#define LEFTENGINEPIN1 7
#define LEFTENGINEPIN2 8

// Right Engine
#define RIGHTENGINEPIN1 9
#define RIGHTENGINEPIN2 10

// PWM Enable Pin
#define ENABLEAPIN 6
#define ENABLEBPIN 5

// Camera Servos
#define horizontalServo 0
#define verticalServo 0

// Infrared Sensors
#define leftIR 0
#define rightIR 0

// Ultrasound Sensors
#define ULTRASOUND_TRIG 13
#define ULTRASOUND_ECHO 11

unsigned long whiteLeft, whiteRight;
bool FLAG_DRIVE = false, FLAG_LOOK_AROUND = false, FLAG_CHECKPOINT= false;
unsigned long timeOnWhite = 0;
bool timeOnWhiteStart = false;
unsigned long MAXTIMEOUT = 2500;
class DCEngine {
  private:
    byte pin1, pin2, pwm_pin;
    
  public:
    DCEngine(byte pin1, byte pin2, byte pwm_pin) {
      this -> pin1 = pin1;
      this -> pin2 = pin2;
      this -> pwm_pin = pwm_pin;

      pinMode(pin1, OUTPUT);
      pinMode(pin2, OUTPUT);
      pinMode(pwm_pin, OUTPUT);
    }

    void drive(int power) {
      if (power < 0){
        analogWrite(this -> pwm_pin, abs(power));
        digitalWrite(this -> pin1, HIGH);
        digitalWrite(this -> pin2, LOW);
      }
      else {
        analogWrite(this -> pwm_pin, power);
        digitalWrite(this -> pin1, LOW);
        digitalWrite(this -> pin2, HIGH);
      }
    }

    void stopMovement(){
      analogWrite(this -> pwm_pin, 0);
    }
};

class TONY {
  private: 
    /*DCEngine leftEngine = DCEngine(LEFTENGINEPIN1, LEFTENGINEPIN2, ENABLEAPIN);
    DCEngine rightEngine = DCEngine(RIGHTENGINEPIN1, RIGHTENGINEPIN2, ENABLEBPIN);*/

  public:
    DCEngine leftEngine = DCEngine(LEFTENGINEPIN1, LEFTENGINEPIN2, ENABLEAPIN);
    DCEngine rightEngine = DCEngine(RIGHTENGINEPIN1, RIGHTENGINEPIN2, ENABLEBPIN);
    
    TONY () {
      /*this -> leftEngine = DCEngine(LEFTENGINEPIN1, LEFTENGINEPIN2, ENABLEAPIN);
      this -> rightEngine = DCEngine(RIGHTENGINEPIN1, RIGHTENGINEPIN2, ENABLEBPIN);*/
    }

    void autoPilot() {
      
    }

    void turnRight(){
      this -> leftEngine.drive(255);
      this -> rightEngine.drive(-255);
      delay(300);
      this -> rightEngine.stopMovement();
      this -> leftEngine.stopMovement();
      
    }

    void turnLeft(){
      this -> leftEngine.drive(-255);
      this -> rightEngine.drive(255);
      delay(300);
      this -> rightEngine.stopMovement();
      this -> leftEngine.stopMovement();
      
    }

    void controlTests() {
      this -> leftEngine.drive(255);
      this -> rightEngine.drive(255);
      delay(1000);
      this -> rightEngine.stopMovement();
      this -> leftEngine.stopMovement();
    }
};

unsigned long calibrateSensor(int pin){
  unsigned long sum = 0;
  int n = 25;
  for(int i = 0; i < n; i++){
    sum += readSensor(pin);
  }

  return sum/n;
}

int readSensor(int pin){
  unsigned long t1, t2;
  unsigned long maxTime = 2000;
  
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
  
  delay(1);
  pinMode(pin, INPUT);
  t1 = micros();

  int t = 0;
   while(digitalRead(pin) == HIGH && t <= maxTime){
    delayMicroseconds(5);
    t += 5;
   }

   t2 = micros() - t1;
   
  return t2;
}

TONY tony;
Servo servoHorizontal, servoVertical;

void setup() {
  Wire.begin(8);                /* join i2c bus with address 8 */
  Wire.onReceive(receiveEvent); /* register receive event */
 
  Serial.begin(9600);
  servoHorizontal.attach(3);
  servoVertical.attach(2);
  servoHorizontal.write(90);
  servoVertical.write(45);

  pinMode(ULTRASOUND_TRIG, OUTPUT);
  pinMode(ULTRASOUND_ECHO, INPUT);
  
  /*Serial.println("Calibrating left");
  whiteLeft = calibrateSensor(4);
  delay(250);
  Serial.println("Calibrating right");
  whiteRight = calibrateSensor(12);
  delay(250);
  Serial.println("Calibration done");
  delay(1000);*/
}

unsigned long left, right, total;
unsigned long black = 500;

void followLine(){
  left = readSensor(12);
  right = readSensor(4); 
  int delayTime = 5;

  //Serial.println(String(left) + " " + String(right));
  
  if(left >= black && right < black) {
    //Serial.println("Turn left");
    tony.leftEngine.drive(-255);
    tony.rightEngine.drive(255);

    MAXTIMEOUT = 3000;
    timeOnWhiteStart = false;
  }
  else if(left < black && right >= black) {
    //Serial.println("Turn right");
    tony.leftEngine.drive(255);
    tony.rightEngine.drive(-255);

    MAXTIMEOUT = 3000;
    timeOnWhiteStart = false;
  }
  else if(left < black && right < black) {
    //Serial.println("Go forward");
    if (!timeOnWhiteStart){
      timeOnWhite = millis();
      timeOnWhiteStart = true;
    }
    
    tony.leftEngine.drive(255);
    tony.rightEngine.drive(255);
  }
  else if(left > black && right > black){
    if (FLAG_CHECKPOINT){
      FLAG_CHECKPOINT = false;
      FLAG_DRIVE = false;

      tony.leftEngine.stopMovement();
      tony.rightEngine.stopMovement();

      delay(5000);

      return;
    }
    else{
      tony.leftEngine.drive(255);
      tony.rightEngine.drive(255);
      return;
    }
  }

  delay(6);
    
  tony.leftEngine.stopMovement();
  tony.rightEngine.stopMovement();

  delay(17);
}

int lookAroundTime = 1000;

void receiveEvent(int howMany) {
  int i = 0, j = 0;
  char cmd[50];
  char val[50];
  bool comma = false;
  
 while (0 <Wire.available()) {
    char c = Wire.read();      /* receive byte as a character */
    //Serial.println(c);
    if (c == '-'){
      //Serial.println(c);
      comma = true;
      continue;
    }

    if (!comma){
      cmd[i]=c;
      i++;
    }
    else
    {
      val[j]=c;
      j++;
    }
  }
  cmd[i] = '\0';
  val[j] = '\0';
  
  if(!strcmp(cmd, "HORIZONTAL_SERVO")){
      //followLine();
      servoHorizontal.write(atoi(val));
   }
   else if(!strcmp(cmd, "VERTICAL_SERVO")){
      servoVertical.write(atoi(val));
   }
    else if(!strcmp(cmd, "FOLLOW_LINE")){
      FLAG_DRIVE = true;
    }
    else if(!strcmp(cmd, "STOP")){
      FLAG_DRIVE = false;
    }
    else if(!strcmp(cmd, "LOOK_AROUND")){
      FLAG_LOOK_AROUND = true;
      if (strlen(val) >= 2){
        lookAroundTime = atoi(val);
      }
    }
    else if(!strcmp(cmd, "STOP_LOOKING")){
      FLAG_LOOK_AROUND = false;
    }
    else if(!strcmp(cmd, "STOP_AT_CHECKPOINT")){
      FLAG_CHECKPOINT = true;
    }
}

int measureDistance() {
  long duration;
  int distance; 

  digitalWrite(ULTRASOUND_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASOUND_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASOUND_TRIG, LOW);
  duration = pulseIn(ULTRASOUND_ECHO, HIGH);
  distance = duration * 0.034 / 2;
  
  return distance;
} 

int hs = 90, vs = 90, hd = 20, vd = 1;
unsigned long ht;

unsigned long lastLookAroundTime = 0;

void lookAround(){ 
  unsigned long timeNow= millis();

  timeOnWhiteStart = false;
  
  if (timeNow - lastLookAroundTime >= lookAroundTime){
    lastLookAroundTime = timeNow;

    servoHorizontal.write(hs);
    hs = hs + hd;
        
    if(hs == 170){
      hd = -20;
    }
    else if(hs == 10){
      hd = 20;
    }
  }
}

unsigned long lastDistanceMeasureTime = 0;
int distanceToObject;
unsigned long timeNow;

void loop() {  
  timeNow = millis();
  
  if (timeNow - lastDistanceMeasureTime >= 500){
    lastDistanceMeasureTime = timeNow;
    distanceToObject = measureDistance();
  }

  if (distanceToObject <= 7){
    
  }
  else {
    if(FLAG_DRIVE){
      followLine();
    }
   }

   if (FLAG_LOOK_AROUND){
      lookAround();
    }
    else{
      timeNow = millis();
     if (timeOnWhiteStart && timeNow - timeOnWhite >= MAXTIMEOUT){
      //Serial.print(timeNow);
      //Serial.print("-");
      //Serial.println(timeOnWhite);
      if(timeOnWhiteStart){
        MAXTIMEOUT += 500;
      }
      timeOnWhiteStart = false;

      tony.turnLeft();
      //Serial.println("TURN");
   }
    }
}
