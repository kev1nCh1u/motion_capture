/*
 * this is a analog with arduino nano
 * create by NTUST Kevin Chiu in 2021
*/


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  Serial.println("start");
  
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(3, OUTPUT);
  
}

void loop() {
  // analogWriteResolution(8);
  analogWrite(11,200);
  analogWrite(10,200);
  analogWrite(9,200);
  analogWrite(6,200);
  analogWrite(5,200);
  analogWrite(3,200);
  delay(2);
}
