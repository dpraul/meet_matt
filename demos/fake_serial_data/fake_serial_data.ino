uint8_t NUM_SHIFT_BITS = 56;
uint8_t NUM_MUX_BITS = 16;

void setup() {
  Serial.begin(115200);

  randomSeed(analogRead(0));
  
  while (!Serial) {}
}

void loop() {
  if (Serial && Serial.read() == 6) {
    for (uint8_t i = 0; i < NUM_SHIFT_BITS; i++) {
      for (uint8_t j = 0; j < NUM_MUX_BITS; j++) {
        sendInt(random(1, 1024));
      }
    }
  }
}

uint16_t MASK = B11111111;
void sendInt(uint16_t num) {
  // write an integer in exactly two pulses
  Serial.write(num >> 8);
  Serial.write(num & MASK);
}

