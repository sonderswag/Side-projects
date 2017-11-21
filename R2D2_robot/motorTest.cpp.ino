
#include "stepper.h"
#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>

using namespace std; 

const int = stepPerRevolution = 200 ; 

int main() 
{
  Stepper motor1(stepPerRevolution, 8,9,10,11); 
  motor1.setSpeed(60); 

  while(1)
  {
    motor1.step(200); 
    _delay_ms(500); 
    motor1.step(-200);
    _delay_ms(500); 
  }


}
