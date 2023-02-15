#include "pitches.h"
// notes in the melody:
int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};
// note durations: 4 = quarter note, 8 = eighth note, etc.:
int noteDurations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};

void play();
unsigned long start_time;
unsigned long current_time;
unsigned long second = 1000;
unsigned long minute = 60000;
unsigned long hour = 360000;
unsigned long num_hours = 10;
unsigned long num_minutes = 0;
unsigned long wake_up = (num_hours * hour) + (num_minutes * minute);


void setup() {
  start_time = millis();
}

void loop() {
  current_time = millis();
  unsigned long times;
  times = current_time - start_time;
  if (times > minute && times < minute + 10 * second) {
    play();
    delay(3000);
    play();
  }
  if (times > minute * 20 && times < (minute * 20) + (10 * second)) {
    play();
    delay(3000);
    play();
  }
  if (times > hour && times < hour + (10 * second)){
    play();
    delay(3000);
    play();
  }
  
  if (times > wake_up) {
    play();
  }

}


void play() {
  // iterate over the notes of the melody:
  for (int thisNote = 0; thisNote < 8; thisNote++) {

    // to calculate the note duration, take one second divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(8, melody[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(8);
  }
}
