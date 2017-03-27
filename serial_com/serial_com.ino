#define FASTADC 1

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

//Mux enable pins
int MUX0_EN = A2;

//Mux control pins
int MUX00 = 9;
int MUX01 = 10;
int MUX02 = 11;
int MUX03 = 12;
int MUX10 = 13;
int MUX11 = 7;
int MUX12 = 4;
int MUX13 = 3;
int MUX_CONTROL[2][4] = {
  {MUX00, MUX01, MUX02, MUX03},
  {MUX10, MUX11, MUX12, MUX13}
};


//Mux in "SIG" pin
int MUX_SIG_0 = A0;
int MUX_SIG_1 = A1;
int MUX_SIG[2] = {MUX_SIG_0, MUX_SIG_1};


//Shift register pins
int latchPin = 5;  // RCLK
int clockPin = 6;  // SRCLK
int dataPin = 2;   // SER

// Bits to cycle
int NUM_SHIFT_BITS = 56;
int NUM_MUX_BITS = 16 + 3;

bool success = true; // used for error checks
int MUX_DELAY_US = 1;
int MIN_SHIFT_DELAY_US = 10;
int SHIFT_DELAY_US = MIN_SHIFT_DELAY_US;


void setup() {
  #if FASTADC
   // set prescale to 16
   sbi(ADCSRA,ADPS2) ;
   cbi(ADCSRA,ADPS1) ;
   cbi(ADCSRA,ADPS0) ;
  #endif
  
  //Mux setup
  for (int i = 0; i < 2; i++) {  // MUX_CHANNEL.length
    for (int j = 0; j < 4; j++) {  // MUX_CHANNEL[0].length
      pinMode(MUX_CONTROL[i][j], OUTPUT);
    }
  }
  pinMode(MUX0_EN, OUTPUT);

  //Shift register setup
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  
  // empty shift registers
  digitalWrite(latchPin, LOW);
  for (int i = 0; i < NUM_SHIFT_BITS; i++) {
    digitalWrite(clockPin, HIGH);
    delayMicroseconds(1);
    digitalWrite(clockPin, LOW);
  }
  digitalWrite(latchPin, HIGH);

  Serial.begin(500000);
}


void loop() {
  if (Serial && Serial.read() == 6) {
    digitalWrite(dataPin, HIGH);
    shiftInDataOnce(SHIFT_DELAY_US);
    digitalWrite(dataPin, LOW);
    for (int j = 0; j < NUM_SHIFT_BITS; j++) {
      for (int i = NUM_MUX_BITS - 1; i >= 0; i--) {
        sendInt(readMux(i));
      }

      // right now this will shift it an extra time
      shiftInDataOnce(SHIFT_DELAY_US);  // go to the next
    }
  }
}

uint16_t MASK = B11111111;
void sendInt(uint16_t num) {
  // write an integer in exactly two pulses
  Serial.write(num >> 8);
  Serial.write(num & MASK);
}


void shiftInDataOnce(int us) {
  /**
   * Shifts in whatever is currently in the dataPin with a delay of the pulse of twice us
   * To shift in high, digitalWrite(dataPin, HIGH) before shiftInDataOnce, then LOW after 
   */
  digitalWrite(latchPin, LOW);
  digitalWrite(clockPin, HIGH);
  delayMicroseconds(us);
  digitalWrite(clockPin, LOW);
  delayMicroseconds(us);
  digitalWrite(latchPin, HIGH);
}


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
  {1, 1, 1, 1}  //channel 15
};

int selectMuxChannel(int which, int channel) {
  //loop through the 4 control pins
  for (int i = 0; i < 4; i ++) {
    digitalWrite(MUX_CONTROL[which][i], muxChannel[channel % 16][i]);
  }
}

int readMux(int channel) {
  int which = channel / 16;
  if (which == 0) {
    digitalWrite(MUX0_EN, LOW);
    selectMuxChannel(1, 8);  // set to unused channel
  }
  else {
    digitalWrite(MUX0_EN, HIGH);
  }
  selectMuxChannel(which, channel);
  delayMicroseconds(MUX_DELAY_US);
  //read the value at the SIG pin
  return analogRead(MUX_SIG[which]);
}

