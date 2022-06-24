/*
 * this is a led_timer_isr with arduino nano
 * create by NTUST Kevin Chiu in 2021
 */

void setup() {
    // https://playground.arduino.cc/Main/TimerPWMCheatsheet/
    TCCR0B = TCCR0B & 0xF8 | 0x01;
  
}

void loop() {

}