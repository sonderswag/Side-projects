from datetime import datetime 

# this updates the lcd disp
def change_disp(text1,text2):
     lcd.clear()
     lcd.backlight(lcd.OFF)
     lcd.backlight(lcd.ON)
     lcd.message(text1+"\n"+text2)


#default messages 
defualt_1 = "David Lee is..."
defualt_time = "" # this will be the date of last email
defulat_3 = "in. Knock / txt"
body_1 = ""
body_2 = ""
body_3 = ""

# Timers
change_disp_1 = 0 # this timer the defualt switching 
defult_switch_timer = 0 
body_timer = 0 # this handles the body swtiching after a certine amount of time 
start_body_timer = 0 # this is the sentinle to start the body timer 

while True: 
     
     getmail() 
     
     # getting information form the new message
     if newest_msg_time != message['date']:
          if message['form'] == "David Lee <David.Lee@gordon.edu>":
               date = str(message['date'])
               subject = str(message['subject'])
               newest_msg_time = date 
               new_msg = 1 
               
     # handles the new message           
     elif new_msg == 1: 
          new_msg = 0
          
          if subject == "": # defulat case 
               start_body_timer = 0 # turning off the body timer tigger (incase it is not already off)
               change_disp_1 = 1 # !!! triggering the default case !!!
               defualt_switch_timer = 0 # resetting the timer
               
          elif "." in subject: # personal message for a set number of min 
               start_body_timer = 1 # This triggers the body timer,
               change_disp_1 = 0 # turning off the defualt switching in case it is on (for now at least)
               time_start = subject.rfind(".")
               body_timer_end = int(subject[time_start+1:len(subject)]) # grabing the number 
               body_1 = str(body).split("\n")[0]
               body_2 = str(body).split("\n")[1]
               body_3 = str(body).split("\n")[2]
               change_disp(body_1,body_2)
               
          else: # personal text changing the defulat 
               change_disp_1 = 3 # !!! triggering the third case for switching !!! 
               
      # handles swtiching the defualt for disp_line one. for when their is an SL = ""  or for when sl = ".#min"        
      elif change_disp_1 != 0
           
           if change_disp_1 == 1: # defualt case
                disp_line_2 = defualt_3 
           elif change_disp_1 == 2: # body text case 
                disp_line_2 = body_3
           elif chaneg_disp_1 == 3: # SL display Text case
                disp_line_2 = subject
          
           if defualt_switch_timer <= 1: 
                change_disp(defualt_1,disp_line_2)
           elif defualt_switch_timer >= 10: 
                defuat_time = datetime.now() # getting the real time for the default switching (may have to restrict)
                change_disp(default_time,disp_line_2)
                defualt_switch_timer = 0 
           defualt_switch_timer += 1 
     
           
     elif body_timer >= body_timer_end: 
          start_body_timer = 0 # this turns off the body timer 
          change_disp_1 = 2 # turns the default switching back on, but this time for the case that disp_2 is the body_3
          defualt_switch_timer = 0 # resetting the swtiching timer
          body_timer = 0 
          
            
     elif start_body_timer == 1: 
          body_timer += 1 
          
          
     time.sleep(1)
          
               
          
               
               
               
          
          
     

