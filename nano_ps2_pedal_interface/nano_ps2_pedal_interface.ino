/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.
 
 This example code is in the public domain.
 */

#include "string.h"

#define BAUD_RATE 57600
#define LOOP_RATE_HZ 500

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUD_RATE);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int pedal_value_1 = analogRead(A6);
  int pedal_value_2 = analogRead(A7);  
  // print out the value you read:
  String string_out;
  string_out = "a" + String(pedal_value_1, DEC) + "b" + String(pedal_value_2, DEC);
  Serial.println(string_out);
  delay(LOOP_RATE_HZ/2);        // delay in between reads for stability
}
