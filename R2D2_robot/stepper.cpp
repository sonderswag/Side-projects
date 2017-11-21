#include "stepper.h"

#include <avr/io.h>
#include <util/delay.h>
#include <stdio.h>



// this is for the stepper function it uses the arduino 8-bit timer 
// see the following link for explination of the function: 
// http://garretlab.web.fc2.com/en/arduino/inside/arduino/wiring.c/micros.html
unsigned long micros() {
    unsigned long m;
    uint8_t oldSREG = SREG, t; // bit values so max of 255 
     
    cli();
    m = timer0_overflow_count;
#if defined(TCNT0)
    t = TCNT0;
#elif defined(TCNT0L)
    t = TCNT0L;
#else
    #error TIMER 0 not defined
#endif
 
   
#ifdef TIFR0
    if ((TIFR0 & _BV(TOV0)) && (t & 255))
        m++;
#else
    if ((TIFR & _BV(TOV0)) && (t & 255))
        m++;
#endif
 
    SREG = oldSREG;
     
    return ((m << 8) + t) * (64 / clockCyclesPerMicrosecond());
}

Stepper::Stepper(int number_of_steps, int motor_pin_1, int motor_pin_2,int motor_pin_3, int motor_pin_4)
{ 
	this->motorPins[0] = motor_pin_0;
	this->motorPins[1] = motor_pin_1;
	this->motorPins[2] = motor_pin_2;
	this->motorPins[3] = motor_pin_3;
	pin_count = 4; 
	step_number = 0; 
	last_step_time = 0; 

	this->number_of_steps = number_of_steps; 

	// initalizing pins to be used as ports 
	for (int i = 0 ; i < 4 ; i++)
	{
		if (motorPins[i] < 8 && motorPins[i] >= 0) //port D 
		{
			DDRD |= (1 << motorPins[i]); 
		}
		else if (motorPins[i] < 14 && motorPins[i] >= 8)  // port B offset by 8 
		{
			DDRB |= (1 << motorPins[i]); 
		}

	}
} 


 /* Moves the motor steps_to_move steps.  If the number is negative,
 * the motor moves in the reverse direction.
 */
void Stepper::step(int steps_to_move)
{
  int steps_left = abs(steps_to_move);  // how many steps to take

  // determine direction based on whether steps_to_mode is + or -:
  if (steps_to_move > 0) { this->direction = 1; }
  if (steps_to_move < 0) { this->direction = 0; }


  // decrement the number of steps, moving one step each time:
  while (steps_left > 0)
  {
    unsigned long now = micros();
    // move only if the appropriate delay has passed:
    if (now - this->last_step_time >= this->step_delay)
    {
      // get the timeStamp of when you stepped:
      this->last_step_time = now;
      // increment or decrement the step number,
      // depending on direction:
      if (this->direction == 1)
      {
        this->step_number++;
        if (this->step_number == this->number_of_steps) {
          this->step_number = 0;
        }
      }
      else
      {
        if (this->step_number == 0) {
          this->step_number = this->number_of_steps;
        }
        this->step_number--;
      }
      // decrement the steps left:
      steps_left--;
      // step the motor to step number 0, 1, ..., {3 or 10}
      if (this->pin_count == 5)
        stepMotor(this->step_number % 10);
      else
        stepMotor(this->step_number % 4);
    }
  }
}


void digitalWrite(int pin_number, int voltage)
{
	if (pin_number < 8 && pin_number >= 0) //port D 
	{
		if (voltage == 1 ) //set pin to high 
		{
			PORTD |= (voltage << pin_number); 
		}
		else if (voltage == 0)
		{
			PORTD &= ~(1 << pin_number); 
		}
	}
	else if (pin_number < 14 && pin_number >= 8)  // port B offset by 8 
	{
		if (voltage == 1 ) //set pin to high 
		{
			PORTB |= (voltage << pin_number); 
		}
		else if (voltage == 0)
		{
			PORTB &= ~(1 << pin_number); 
		}
	}

}
/*
 * Moves the motor forward or backwards.
 */
void Stepper::stepMotor(int thisStep)
{
	#define LOW = 0 ; 
	#define High = 1 ; 
  
  if (this->pin_count == 4) {
    switch (thisStep) {
      case 0:  // 1010
        digitalWrite(motorPins[1], HIGH);
        digitalWrite(motorPins[2], LOW);
        digitalWrite(motorPins[3], HIGH);
        digitalWrite(motorPins[4], LOW);
      break;
      case 1:  // 0110
        digitalWrite(motorPins[1], LOW);
        digitalWrite(motorPins[2], HIGH);
        digitalWrite(motorPins[3], HIGH);
        digitalWrite(motorPins[4], LOW);
      break;
      case 2:  //0101
        digitalWrite(motorPins[1], LOW);
        digitalWrite(motorPins[2], HIGH);
        digitalWrite(motorPins[4], LOW);
        digitalWrite(motorPins[5], HIGH);
      break;
      case 3:  //1001
        digitalWrite(motorPins[1], HIGH);
        digitalWrite(motorPins[2], LOW);
        digitalWrite(motorPins[3], LOW);
        digitalWrite(motorPins[4], HIGH);
      break;
    }
  }

/*
 * Sets the speed in revs per minute
 */
void Stepper::setSpeed(long whatSpeed)
{
  this->step_delay = 60L * 1000L * 1000L / this->number_of_steps / whatSpeed;
}