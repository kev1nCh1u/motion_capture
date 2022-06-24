/*
 * this is a led_timer with arduino nano
 * create by NTUST Kevin Chiu in 2021
 */

#include <arduino-timer.h>

auto timer = timer_create_default(); // create a timer with default settings

bool ledStart[6] = {0, 1, 0, 1, 0, 1};
int ledSet[6] = {1, 1, 2, 2, 3, 3};
int ledCount[6];
int ledPin[6] = {11, 10, 9, 6, 5, 3};



bool toggle_led(void *) {

  for(int i=0; i<6; i++)
  {
    ledCount[i]++;
    if(ledCount[i] >= ledSet[i])
    {
      digitalWrite(ledPin[i], !digitalRead(ledPin[i])); // toggle the LED
      ledCount[i] = 0;
    }
  }

  return true; // repeat? true
}

void setup() {
  for(int i=0; i<6; i++)
  {
    pinMode(ledPin[i], OUTPUT); // set LED pin to OUTPUT
    digitalWrite(ledPin[i], ledStart[i]);

  }

  // call the toggle_led function every 1000 millis (1 second)
  timer.every(1000/100, toggle_led);
}

void loop() {
  timer.tick(); // tick the timer
}
