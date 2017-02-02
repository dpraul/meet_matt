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


void setup(){
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

  Serial.begin(9600);
}


void loop(){
  leds = 0;
  updateShiftRegister();
  for (int j = 5; j < 8; j++)
  {
    bitSet(leds, j);
    updateShiftRegister();
    
    //Loop through and read all 16 values
    //Reports back Value at channel 6 is: 346
    for(int i = 0; i < 3; i ++){
      selectChannel(i);
      Serial.print("Selected channel ");
      Serial.print(j);
      Serial.print(",");
      Serial.print(i);
      Serial.print(": ");
      Serial.print(readMux(i));
      Serial.println();
      delay(500);
    }
    
    bitClear(leds, j);
  }
}

void updateShiftRegister()
{
   digitalWrite(latchPin, LOW);
   shiftOut(dataPin, clockPin, LSBFIRST, leds);
   digitalWrite(latchPin, HIGH);
}

int controlPin[] = {s0, s1, s2, s3};

int muxChannel[16][4]={
  {0,0,0,0}, //channel 0
  {1,0,0,0}, //channel 1
  {0,1,0,0}, //channel 2
  {1,1,0,0}, //channel 3
  {0,0,1,0}, //channel 4
  {1,0,1,0}, //channel 5
  {0,1,1,0}, //channel 6
  {1,1,1,0}, //channel 7
  {0,0,0,1}, //channel 8
  {1,0,0,1}, //channel 9
  {0,1,0,1}, //channel 10
  {1,1,0,1}, //channel 11
  {0,0,1,1}, //channel 12
  {1,0,1,1}, //channel 13
  {0,1,1,1}, //channel 14
  {1,1,1,1}  //channel 15
};

int readMux(int channel){
  //loop through the 4 sig
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
  int val = analogRead(SIG_pin);

  //return the value
  return val;
}

int selectChannel(int channel){
  //loop through the 4 sig
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
}
