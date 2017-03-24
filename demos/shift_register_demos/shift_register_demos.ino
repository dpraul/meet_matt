//Shift register pins
int latchPin = 5;  // RCLK
int clockPin = 6;  // SRCLK
int dataPin = 2;   // SER

int NUM_PINS = 16;
int MIN_SHIFT_DELAY_US = 10;
int shift_delay_us = 50;


void setup() {
  //Shift register setup
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);

  digitalWrite(latchPin, LOW);
  // empty shift registers
  for (int i = 0; i < NUM_PINS; i++) {
    digitalWrite(clockPin, HIGH);
    delayMicroseconds(1);
    digitalWrite(clockPin, LOW);
  }
  digitalWrite(latchPin, HIGH);
}


void loop() {
  shiftBitThroughAll();
}

void shiftInDataOnce(int us) {
  /**
   * Shifts in whatever is currently in the dataPin with a delay of the pulse of twice us
   * To shift in high, digitalWrite(dataPin, HIGH) before shiftInDataOnce, then LOW after 
   */
  digitalWrite(latchPin, LOW);
  digitalWrite(clockPin, HIGH);
  delay(us);
  digitalWrite(clockPin, LOW);
  delay(us);
  digitalWrite(latchPin, HIGH);
}

void shiftBitThroughAll() {
  digitalWrite(dataPin, HIGH);
  shiftInDataOnce(shift_delay_us);
  digitalWrite(dataPin, LOW);
  for (int i = 0; i < NUM_PINS - 1; i++) {  // shift once less because shifts once for data in
    // can read data here
    shiftInDataOnce(shift_delay_us);
  }
}

