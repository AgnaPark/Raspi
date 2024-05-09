#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); //0x27
Servo servo;
int angle = 90;

const int trigPinEntrance = 7;
const int echoPinEntrance = 8;

const int trigPinExit = 9;
const int echoPinExit = 10;

const int ledPin = 3;

float duration1, duration2;
float distance1, distance2;

void setup() {
  Serial.begin(9600);

  // Lcd Setup
  lcd.begin();
  lcd.backlight();

  // Ultrasonic Setup
  pinMode(trigPinEntrance, OUTPUT);
  pinMode(echoPinEntrance, INPUT);

  pinMode(trigPinExit, OUTPUT);
  pinMode(echoPinExit, INPUT);

  digitalWrite(trigPinEntrance, LOW);
  digitalWrite(trigPinExit, LOW);

  // LED Setup
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  
  // Servo Setup
  angle = 90;
  servo.write(angle);
}


void loop() 
{ 
  // Ultrasonic Signaling  
  digitalWrite(trigPinEntrance, LOW);
  digitalWrite(trigPinExit, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinEntrance, HIGH);
  digitalWrite(trigPinExit, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinEntrance, LOW);
  digitalWrite(trigPinExit, LOW);

  duration1 = pulseIn(echoPinEntrance, HIGH);
  duration2 = pulseIn(echoPinExit, HIGH);

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
  Serial.print(distance1);
  Serial.print(" Dist2: ");
  Serial.println(distance2);

  // If car at entrance
  if(distance1 < 10){
    // move from 90 to 180 degrees
    for(; angle <= 180; angle++)  
      {                                  
        servo.write(angle);               
        delay(15);                   
      }             
     
  }else{
    // reverse from 180 to 90 degrees   
    for( ;angle >= 90; angle--)    
    {                                
      servo.write(angle);           
      delay(15);       
    }
  }
/*
  // If car at exit
  if(distance2 < 10){
    // move from 90 to 180 degrees
    for(; angle <= 180; angle++)  
      {                                  
        servo.write(angle);               
        delay(15);                   
      }
  }else{
    // reverse from 180 to 0 degrees
    for(; angle >= 90; angle--)    
    {                                
      servo.write(angle);           
      delay(15);       
    }
  }
  */
  Serial.print(angle);
} 