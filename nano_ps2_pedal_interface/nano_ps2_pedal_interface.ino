#include "string.h"

#define BAUD_RATE 57600
#define LOOP_RATE_HZ 500

const int pedal_1_upper = 920;
const int pedal_1_lower = 560;
const int pedal_2_upper = 1023;
const int pedal_2_lower = 740;

const int output_upper = 1024;
const int output_lower = 0;

boolean flip_output = true;

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  int pedal_value_1 = 0;
  int pedal_value_2 = 0;
  if (!flip_output){
    pedal_value_1 = map(analogRead(A4), pedal_1_lower, pedal_1_upper, output_lower, output_upper);
    pedal_value_2 = map(analogRead(A6), pedal_2_lower, pedal_2_upper, output_lower, output_upper);
  } else {
    pedal_value_1 = map(analogRead(A4), pedal_1_lower, pedal_1_upper, output_upper, output_lower);
    pedal_value_2 = map(analogRead(A6), pedal_2_lower, pedal_2_upper, output_upper, output_lower);
  }
  String string_out;
  string_out = String(pedal_value_1, DEC) + "b" + String(pedal_value_2, DEC);
  Serial.println(string_out);
  delay(LOOP_RATE_HZ/2);        // delay in between reads for stability
}
