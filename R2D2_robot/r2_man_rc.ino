#include <Stepper.h>

// prescale = 1024
// needed for the rc pulse reading 
#define max_clock_count 62499
#define num_rc_pins 2 
const int rc_pins[num_rc_pins] = {1,2} ; // pins for the rc the number is the correct place in a 
 int pulse_rise[num_rc_pins]; // this will keep track of the rising edge of the PWM 
 int rc_pulse_width[num_rc_pins]; // stores the width of the PWM singal for each input pin 
 int rc_pin_state[num_rc_pins] = {0,0}; //stores wheater the pin is high or low 

// for motor control 
int axis_values[2] = {0,0}; 
const int stepsPerRevolution = 200; 
int rate[2] = {0,0};
Stepper motor_R(stepsPerRevolution, 6, 7, 8, 9);
Stepper motor_L(stepsPerRevolution, 10, 11, 12, 13);

/* Function: pin change interrupt Setup_digital 
 * Purpose: used to set up pin interrupt in order to read the pwm 
 * inputs: int array of port C pins to enable the interrupt on 
 * outputs: none 
 * Notes: This is only set up to read pin from Port C (all the A inputs on UNO) 
 *  must be in sequential order 
*/
void pciSetup_Digital(const int* pins)
{

  cli(); // clearing interrups 
  Serial.println("set up pin");
  PCICR |= 1 << PCIE1 ; // enabling interrupts on port C
  // enabling indivudal pins in port C
  for (int i = 0; i < sizeof(pins) ; i++) 
  {
    PCMSK1 |= 1 << pins[i] ;
  }
  sei() ; // global interrupt enable 

}

/* Function: int_timer1 
 * Purpose: to initalize the 16bit timer to be used for PWM reading 
 * inputs / outputs : none 
 */
void int_timer1()
{
  cli(); 
  TCCR1A = 0; 
  TCCR1B = 0; 
  TCNT1 = 0; 
  OCR1A = max_clock_count; // set the number of clock counts to interrupt on 
  TCCR1B |= (1 << WGM12); //set timer to clear timer on compare mode 

  TCCR1B |= (1<< CS12) ;
  TCCR1B |= (1 << CS10); // setting prescale to 101 aslo starts timer 
  TIMSK1 |= (1 << OCIE1A); // enable clock interrupt
  sei(); 
  //the counter is stored in TCNT1 16 bit number 
}

/* Port c pin change interrupt 
 * Purpose: will be activated everytime there is a change of value in
 *  monitored pin. From this will be able to determine the width of PWM 
 *  signal 
 */
ISR(PCINT1_vect)
{

  // for loop to loop over all rc pins to look for which pin changed, 
  // and update it's state 
  for (int i =0; i < num_rc_pins ; i++) 
  {
    // determining the current state of all active pins 
    int cur_value = ((PINC & (1 << rc_pins[i]) ) != 0) ;
    
    if (rc_pin_state[i] != cur_value) // if change in state
      {
        if (cur_value == 0) // falling 
        {
//          Serial.println(TCNT1); 
          rc_pin_state[i] = 0; 
//          pulse_fall[i] = TCNT1; 
          rc_pulse_width[i] = pulse_rise[i] - TCNT1; 
        }
        else //rising 
        {
          rc_pin_state[i] = 1; 
          pulse_rise[i] = TCNT1; 
        }
      }
  }
}

//timer interrupt, need to adjust the rise clk count in case of overflow
ISR(TIMER1_COMPA_vect)
{
  Serial.println("timer interrupt"); 
  for (int i =0; i < num_rc_pins ; i ++)
  {
    pulse_rise[i] = pulse_rise[i] - max_clock_count; 
  }
}

/* function: get_motorSpeeds 
purpose: get the speed from the rc reciever 
inputs: 
  y_pin & x_pin  : the pin on arduinothe y_axis of rc singal in plugged into 
  axis_v: pointer to int array of len two that holds the axis position 
    after processing. [0] = y-axis , [1] = x-axis 
  x_prev & y_prev: the last recieved pulse value 
*/ 
void get_motorSpeeds() 
{

  int y_max = 90 ; 
  int x_max = 90 ;
  
  int y_value = rc_pulse_width[0]+24 ; 
  int x_value = rc_pulse_width[1]+24 ; 
//  Serial.println(y_value); 
// running the values through a s shaped function to provide smoother 

//  Serial.println(y_value);  
  y_value = y_value*20 ; 
  x_value = x_value*20 ; 
  axis_values[0] = (y_max / (1 + exp(-.05*y_value+4))) - (y_max / (1 + exp(.05*y_value+4)))  ;
  axis_values[1] = (x_max / (1 + exp(-.05*x_value+4))) - (x_max / (1 + exp(.05*x_value+4)))  ;
  Serial.println(axis_values[0]); 
 
}

void differential_drive()
{
  // rate[0] == left motor
  // rate[1] == right motor 
  // axis_values[0] == y_axis 
  // axis_values[1] == x_axis 

  int y = axis_values[0];
  int x = -axis_values[1]; 

  if ((abs(x) < 5) && (abs(y) < 5)) 
  {
    rate[0] = 0; 
    rate[1] = 0; 
    return ; 
  }

  float z = sqrt(x * x + y * y);
  float rad = acos(abs(x) / abs(z)) ; // convert angel between x and y 
  if (isnan(rad) == true) rad = 0 ; // handle  the non real value 
  float degree = rad * 180 / PI ; 

  /* This is Where things get interesting. The turn coefficient is what determines
   *  how sensitive the motors are to the turn. the range of values for it is [-1,1]. 
   *  1 == going straight, -1 pure turn. 
   *       y
   *   x   |
   *    \  |
   *     \ |
   * x____\|_______
   *       |
   *       |
   */
  float turn_coef = -1 + (degree / 90) * 2; 
  float turn = turn_coef * abs(abs(y) - abs(x)); //multiply by differiential 
  turn = round(turn *100) / 100 ; // normalize to 100 scale 

  float moving = max(abs(y), abs(x)); 
  
  // polarity of which motor gets the turn and which the top moving speed
  if ( ( x >= 0 && y >= 0) || ( x < 0 && y < 0))
  {
    rate[0] = moving; rate[1] = turn;
  }
  else 
  {
    rate[0] = turn; rate[1] = moving; 
  }

  //if y is neg need to switch the polarity 
  if (y < 0) 
  {
    rate[0] = 0 - rate[0]; 
    rate[1] = 0 - rate[1]; 
  }


}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600) ;
  pciSetup_Digital(rc_pins);
  int_timer1(); 

}

void loop() {
  get_motorSpeeds(); 
  differential_drive();  
//  Serial.println(axis_values[0]);
//  Serial.println(axis_values[0]); 
//  Serial.println(PINC );
  // put your main code here, to run repeatedly:

  // left motor 
  if (rate[0] != 0  )
  {
    int dir_L = 1; 
    if (rate[0] < 0) dir_L = -1; 
    motor_L.setSpeed(abs(rate[0]));
    motor_L.step(dir_L*-2);
  }

  // right motor 
  if (rate[1] != 0)
  {
    Serial.println(rate[1]); 
    int dir_R = 1; 
    if (rate[1] < 0) dir_R = -1; 
    motor_R.setSpeed(abs(rate[1]));
    motor_R.step(dir_R*2);
  }
}
