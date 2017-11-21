

// prescale = 1024
#define max_clock_count 62499
#define num_rc_pins 2 
const int rc_pins[num_rc_pins] = {1,2} ;
 int pulse_rise[num_rc_pins]; 
 int pulse_fall[num_rc_pins]; 
 int rc_pulse_width[num_rc_pins]; 
 int rc_pin_state[num_rc_pins] = {0,0}; 

// used to set up pin interrupt
// will only work for port C
void pciSetup_Digital(const int* pins)
{
//  if (pin <= 7) // PORT D 
//  {
//    PCICR |= 1 << 2 ; 
//    PCMSK2 |= 1 << pin ; 
//  }
//  else if (pin <= 13) 
//  {
//    PCICR |= 1 << 0 ; // PORT B
//    pin = pin - 8 ; 
//    PCMSK0 |= 1 << pin ; 
//  }
  cli(); 
  Serial.println("set up pin");
  PCICR |= 1 << PCIE1 ; 
  for (int i = 0; i < sizeof(pins) ; i++) 
  {
    PCMSK1 |= 1 << pins[i] ;
  }
  sei() ;

}

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

// Port c pin change interrupt 
ISR(PCINT1_vect)
{
//  Serial.println("pin change"); 
  for (int i =0; i < num_rc_pins ; i++) 
  {
    int cur_value = ((PINC & (1 << rc_pins[i]) ) != 0) ;
    
    if (rc_pin_state[i] != cur_value)
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

//timer interrupt 
ISR(TIMER1_COMPA_vect)
{
  Serial.println("timer interrupt"); 
  for (int i =0; i < num_rc_pins ; i ++)
  {
    pulse_rise[i] = pulse_rise[i] - max_clock_count; 
  }
}




void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600) ;
  pciSetup_Digital(rc_pins);
  int_timer1(); 
}

void loop() {
  Serial.println(rc_pulse_width[1]); 
//  Serial.println(PINC );
  // put your main code here, to run repeatedly:

}
