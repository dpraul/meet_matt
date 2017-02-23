#include <ArduinoJson.h>
// size of buffer might need to be increased
#define SENSORDATA_JSON_SIZE 200

//Mux control pins
int s0 = 9;
int s1 = 10;
int s2 = 11;
int s3 = 12;

//Mux in "SIG" pin
int SIG_pin = A0;

// enable pin
int EN_pin = 4;

//Shift register pins
int latchPin = 5;
int clockPin = 6;
int dataPin = 2;

byte leds = 0;
bool success = true; // make sure the

int mux_delay = 2;


void setup() {
  //Mux setup
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);

  digitalWrite(EN_pin, LOW);

  //Shift register setup
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);

  Serial.begin(115200);
}


void loop() {
  if (Serial) {
    Serial.readString();
    leds = 0;
    updateShiftRegister();
    StaticJsonBuffer<SENSORDATA_JSON_SIZE> jsonBuffer;
    JsonObject& jsonRoot = jsonBuffer.createObject();
    JsonArray& dataRows = jsonRoot.createNestedArray("data");  // initialize data array in JSON
  
    for (int j = 4; j < 8; j++) {
      JsonArray& row = dataRows.createNestedArray();
      bitSet(leds, j);
      updateShiftRegister();
  
      // each data point is a column point added to a row, which is appended to the whole array.
      for (int i = 0; i < 4; i ++) {
        selectChannel(i);
        success = row.add(readMux(i));  // row.add() responds with whether it worked.
        if (!success) {  // exceeded buffer -- send the error over serial. Increase at top of file.
          Serial.println("{\"error\": \"Exceeded buffer\"}");
        }
        delay(mux_delay);
      }
  
      bitClear(leds, j);
    }
    jsonRoot.printTo(Serial);
    Serial.println();
  }
}

void updateShiftRegister() {
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, leds);
  digitalWrite(latchPin, HIGH);
}

int controlPin[] = {s0, s1, s2, s3};

int muxChannel[16][4] = {
  {0, 0, 0, 0}, //channel 0
  {1, 0, 0, 0}, //channel 1
  {0, 1, 0, 0}, //channel 2
  {1, 1, 0, 0}, //channel 3
  {0, 0, 1, 0}, //channel 4
  {1, 0, 1, 0}, //channel 5
  {0, 1, 1, 0}, //channel 6
  {1, 1, 1, 0}, //channel 7
  {0, 0, 0, 1}, //channel 8
  {1, 0, 0, 1}, //channel 9
  {0, 1, 0, 1}, //channel 10
  {1, 1, 0, 1}, //channel 11
  {0, 0, 1, 1}, //channel 12
  {1, 0, 1, 1}, //channel 13
  {0, 1, 1, 1}, //channel 14
  {1, 1, 1, 1} //channel 15
};

int readMux(int channel) {
  //loop through the 4 sig
  for (int i = 0; i < 4; i ++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
  int val = analogRead(SIG_pin);

  //return the value
  return val;
}

int selectChannel(int channel) {
  //loop through the 4 sig
  for (int i = 0; i < 4; i ++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
}
