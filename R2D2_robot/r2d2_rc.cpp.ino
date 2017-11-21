// me playing around making my own pulse in (kinda works for 1 channel) 
#include <Stepper.h>

/* function: get_motorSpeeds 
purpose: get the speed from the rc reciever 
inputs: 
  y_pin & x_pin  : the pin on arduinothe y_axis of rc singal in plugged into 
  axis_v: pointer to int array of len two that holds the axis position 
    after processing. [0] = y-axis , [1] = x-axis 
  x_prev & y_prev: the last recieved pulse value 
*/ 
void get_motorSpeeds(int y_pin, int x_pin, int* axis_v, int& x_prev, int& y_prev) 
{
  int sp[2] = {0,0}; 

  int sample = 6000; // this is the timeout for the pulse in. used to speed up looping
  // problem is too small miss singal. too big loop too slow for motor  (need like a thread or interrupt) 
  int y_max = 10; 
  int x_max = 5 ;
  
  int y_value = pulseIn(y_pin,HIGH,sample); 
  if (y_value == 0) y_value = y_prev; 
  else y_prev = y_value; 
//  Serial.println(y_prev);

   
  int x_value = pulseIn(x_pin,HIGH,sample); 
  if (x_value == 0) x_value = x_prev; 
  else x_prev = x_value; 
  
// running the values through a s shaped function to provide smoother 
// transisition. 
  y_value = y_value - 1492; 
  x_value = x_value - 1485; 
//  Serial.println(y_value);  
  axis_v[0] = (y_max / (1 + exp(-.1*y_value+2.5))) -10 
    (y_max / (1 + exp(.1*y_value+2.5)))  ;
  axis_v[1] = (x_max / (1 + exp(-.1*x_value+2.5))) -
    (x_max / (1 + exp(.1*x_value+2.5)))  ; 
 
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600) ;
  
}

const int stepsPerRevolution = 200; 
Stepper motor_R(stepsPerRevolution, 6, 7, 8, 9);
Stepper motor_L(stepsPerRevolution, 10, 11, 12, 13);
int axis_values[2] = {0,0};
int rate = 0; 
int x_rate = 0; 
int y_rate = 0; 


void loop() { 
   
  get_motorSpeeds(2,3,axis_values,x_rate,y_rate); 
//  Serial.println(sps[0]); 

  if (axis_values[0] != 0)
  {
    int dir = 1; 
    if (axis_values[0] < 0) dir = -1; 
   
    rate = abs(axis_values[0]*9); 
//    Serial.println("move"); 
    Serial.println(rate); 
    motor_R.setSpeed(rate);
    motor_L.setSpeed(rate);
    motor_R.step(dir*2);
    motor_L.step(dir*-2);
  }
 
}
