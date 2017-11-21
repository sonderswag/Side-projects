import pygame 
from time import sleep
from datetime import datetime
import urllib 
from os import remove

# What this program does. 
# this program is deisgn to be a little internet clock that will be integrated with a touch screen. 
# when when a certine portion of the screen is pushed the program will display some information. 
# imformation to be displayed. 
#  weather: This screen will have the current weather, including temp and conditions. It will also display tonights weather. 
#     There will be a button that can be pressed to display tomorrow's weather. 
#     There will need to be either a button or time limit to change the screen back to the time. In order to do this 
#     I will have to import/export the time when the screen was created. The best way would be to use a while loop that will 
#     break when the screen is to be changed back to the clock. 
#  emial: This screen will display if how many new emials i have recieved and whom they are from. 
#  schedule: this will be the complicated one. 
#     I will have to create an xml file that stores my current class schedule (or possible a program that can read my calender and create a daily xml file with that day's schedule Hmmm)
#     This program will just read the xml file and display todays events in a list. (I will have to see if font render can do multiple lines)
#     If not then i will probably have to use a recursive function to create the font surfaces that will be needed for the events. It will need to destroy the font surfaces when the screen changes.
# in fact i should create a function that will create the font surfaces, and also destroy a given surface. There is no point in having these surfaces just floating around when they are not being used. 


# init the various things that need to run the program
pygame.init()
pygame.font.init()

# defining colors 
white = (255,255,255)
black = (0,0,0)
red = (150,0,0)
green = (0,150,0)
blue = (0,0,150)

# init the screen
width = 310
height = 240
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('test')

# main_background screen for the time and the current weather 
main_background = pygame.Surface(screen.get_size())
main_background = main_background.convert()
main_background.fill(black)

alt_background = pygame.Surface(screen.get_size())
alt_background = alt_background.convert()
alt_background.fill(black)

# weather screen 
weather_screen = pygame.Surface(screen.get_size())

# this is creating a font surface to be render to another surface
time_text = pygame.font.Font(None,40)
date_text = pygame.font.Font(None,30)
button = pygame.font.Font(None,20)
temp = pygame.font.Font(None,25)

# drawing the buttons for time
'''
pygame.draw.rect(main_background,red,(width/6,(2*height)/3,100,50))
main_background.blit(button.render('Current',1,white),((width/6)+25,((2*height)/3)+20))
pygame.draw.rect(main_background,blue,((width/6)+110,(2*height)/3,100,50))
main_background.blit(button.render("Tonight's",1,white),((width/6)+130,((2*height)/3)+20))'''

'''
# drawing the buttons for current weather
pygame.draw.rect(alt_background,red,((4*width)/6,(1*height)/3,100,50)) # this is creating the button for time. 
alt_background.blit(button.render('Time',1,white),((width/6)+30,((2*height)/3)+20)) # this is writting the the words 
#pygame.draw.rect(alt_background,blue,((width/6)+110,(2*height)/3,100,50))
#alt_background.blit(button.render("Tonight's",1,white),((width/6)+140,((2*height)/3)+20))'''


# blit(surface,(x,y)) this will draw a surface on to another surface
# font.render("text",1,(r,g,b)) # this will draw text to the surface created by the font. 

# this is for downloading images, it is the user client. 
class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

#create an opener, so we can change its user-agent
urlopen = MyOpener().open
urlretrieve = MyOpener().retrieve

# this is the command to get the image of the current weather
#urllib.urlretrieve("http://japancsaj.com/pic/susu/Susu_2.jpg", "out.jpg")


# this function handles the clock screen, including...
# getting the time for the local clock 
# writting it to the screen 
# resetting the screen to display the changed time or date 
# last_min is the min displayed the last time the function was called. If the current min is different then last_min then the time will change
# last_date same thing as last_min but with the date. 
def time_date(last_min,last_date,time_screen): 

   current_time = str(datetime.now())
   current_date = current_time[0:10]
   current_min = current_time[10:16]

   if current_min != last_min or current_date != last_date or time_screen == 1:
		time_screen = 0 
		last_min = current_min
		last_date = current_date 
		screen.blit(main_background,(0,0))
		screen.blit(time_text.render(current_min,1,white),((width/3)+10,(height/4)+40))
		screen.blit(date_text.render(current_date,1,white),((width/3),height/4))
		pygame.display.update()
		return last_min,last_date,time_screen

   else: 
      return current_min,current_date,time_screen


# this function will handle getting weather info from the local weather website 
def weather_current(): 
   # connecting to local weather website
   connection = urllib.urlopen("http://www.wbz.com/weather")
   weather = connection.read() # reading the html of website, turning the information into a local construct
   connection.close() # closing the connecitong 

   # finding reference points to begin searching for various weather information 
   current_weather = weather.find("<!-- current conditions -->")

   # extracting various info from the references, will be -1 if the find function was unable to find anythin
   if current_weather != -1 : 
      current_temp_location = weather.find("&deg;",current_weather)
      current_temp = weather[current_temp_location-2:current_temp_location]
      current_pic_start = weather.find('src=',current_weather)
      current_pic_stop = weather.find('" ',current_pic_start)
      urllib.urlretrieve(weather[current_pic_start+5:current_pic_stop], "weather.jpg") # weather img
      return current_temp 

def weather_current_display():
	c_temp = weather_current()
	screen.blit(alt_background,(0,0))
	screen.blit(temp.render("the current temp is "+c_temp,1,white),(5,(height/4)+30))
	image_surface = pygame.image.load('weather.jpg')
	remove('weather.jpg')
	screen.blit(image_surface,(0,0))
	pygame.display.update()
	t = 0 
	while t < 30: 
		time_screen = 1 
		for event in pygame.event.get():
			pygame.event.pump()
			if event.type == pygame.MOUSEBUTTONDOWN:
				[pos_x,pos_y] = pygame.mouse.get_pos()
			 	if button_left(pos_x,pos_y): 
			 		pos_x = 0 
			 		pos_y = 0 
			 		return 
		t +=1 
		sleep(.5)



def weather_tonight(): 
	# connecting to local weather website
   connection = urllib.urlopen("http://www.wbz.com/weather")
   weather = connection.read() # reading the html of website, turning the information into a local construct
   connection.close() # closing the connecitong 

   # finding reference points to begin searching for various weather information
   # returns the desired information 
   tonight_weather = weather.find('class="tonight"')	
   if tonight_weather != -1 : 
   	tonight_temp_location = weather.find("&deg;",tonight_weather)
   	tonight_temp = weather[tonight_temp_location-2:tonight_temp_location]
   	tonight_cond_start = weather.find('"desc_cond">',tonight_weather)
   	tonight_cond_stop = weather.find('</div>',tonight_cond_start)
   	tonight_cond = weather[tonight_cond_start+12:tonight_cond_stop]
   	tonight_img_start = weather.find("src=",tonight_weather)
   	tonight_img_stop = weather.find('" style',tonight_img_start)
   	weather[tonight_img_start+5:tonight_img_stop]

   	urllib.urlretrieve(weather[tonight_img_start+5:tonight_img_stop], "weather.jpg") # weather img
   	return tonight_cond,tonight_temp

def weather_tonight_display(): 
	[t_con,t_temp] = weather_tonight()	
	screen.blit(alt_background,(0,0))
	screen.blit(temp.render("tonights's temp: "+t_temp,1,white),(25,(height/4)+30))
	screen.blit(temp.render("Conditions: "+t_con,1,white),(25,(height/4)+50))
	image_surface = pygame.image.load('weather.jpg')
	remove('weather.jpg')
	screen.blit(image_surface,(0,0))
	pygame.display.update()
	t = 0 
	while t < 30: 
		time_screen = 1 
		for event in pygame.event.get():
			pygame.event.pump()
			if event.type == pygame.MOUSEBUTTONDOWN:
				[pos_x,pos_y] = pygame.mouse.get_pos()
			 	if button_left(pos_x,pos_y): 
			 		pos_y = 0 
			 		pos_x = 0 
			 		return 
		t +=1 
		sleep(.5)


def button_left(posx,posy): 
	if posx >= width/6 and posx <= (width/6)+100 and posy >= (2*height)/3 and posy <= ((2*height)/3)+50:
		return True
	else :
		return False 

def button_right(posx,posy):
	if posx >= (width/6)+110 and posx <= (width/6)+210 and posy >= (2*height)/3 and posy <= ((2*height)/3)+50: 
		return True 
	else: 
		return False

#def button_ up(posx,posy): 
#	pass

# main function of the program. It just needs to be called in order to run everything.
# it has a while loop that will keep the program running. 
def main():
   # priming the pump 
   time_screen = 1 
   last_min = 0 
   last_date = 0 
   while True: 
   		x = pygame.event.get()
   		x = 0    
   		[last_min,last_date,time_screen] = time_date(last_min,last_date,time_screen)
   		for event in pygame.event.get():
   			pygame.event.pump()
   			if event.type == pygame.MOUSEBUTTONDOWN:
 					[posx,posy] = pygame.mouse.get_pos()
 					if button_left(posx,posy): 
 						weather_current_display()

 					elif button_right(posx,posy): 
						weather_tonight_display()

   sleep(2)

main()



