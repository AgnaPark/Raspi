#include <Servo.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2);
Servo servo;
int angle = 10;

const int trigPinEntrance = 7;
const int echoPinEntrance = 8;

const int trigPinExit = 9;
const int echoExit = 10;

float duration1, duration2;
float distance1, distance2;

void setup() {
  Serial.begin(9600);

  // Lcd Setup
  lcd.begin();
  lcd.backlight();

  // Servo Setup
  servo.attach(8);
  servo.write(angle);

  // Ultrasonic Setup
  digitalWrite(trigPin1, LOW);
  digitalWrite(trigPin2, LOW);
}


void loop() 
{ 
  // Ultrasonic Signaling  
  digitalWrite(trigPin1, HIGH);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  digitalWrite(trigPin2, LOW);

  duration1 = pulseIn(echoPin1, HIGH);
  duration2 = pulseIn(echoPin2, HIGH);

  distance1 = (duration1*.0343)/2;
  distance2 = (duration2*.0343)/2;
  
  // Lcd Print
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Dist1: ");
  lcd.setCursor(7,0);
  lcd.print(distance1);
  lcd.setCursor(0,1);
  lcd.print("Dist2: ");
  lcd.setCursor(7,1);
  lcd.print(distance2);

  // Serial Debug
  Serial.print("Dist1: ");
  Serial.print(distance);
  Serial.print(" Dist2: ");
  Serial.println(distance);

  // If car at entrance
  if(distance1 < 10){
    // move from 0 to 180 degrees
    for(angle = 90; angle <= 180; angle++)  
    {                                  
      servo.write(angle);               
      delay(15);                   
    } 
  }else{
    // reverse from 180 to 0 degrees
    for(angle = 180; angle >= 90; angle--)    
    {                                
      servo.write(angle);           
      delay(15);       
    } 
  }

  // If car at exit
  if(distance2 < 10){
    // move from 0 to 180 degrees
    for(angle = 90; angle <= 180; angle++)  
    {                                  
      servo.write(angle);               
      delay(15);                   
    } 
  }else{
    // reverse from 180 to 0 degrees
    for(angle = 180; angle >= 90; angle--)    
    {                                
      servo.write(angle);           
      delay(15);       
    } 
  }
}