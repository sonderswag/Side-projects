import pygame 
from time import sleep
from datetime import datetime
import urllib 
from os import remove

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

# this is creating a font surface to be render to another surface 
time_text = pygame.font.Font(None,40)
date_text = pygame.font.Font(None,30)
button = pygame.font.Font(None,20)
temp = pygame.font.Font(None,25)

# main_background screen for the time and the current weather that can be blit to the main pygame screen. 
main_background = pygame.Surface(screen.get_size())
main_background = main_background.convert()
main_background.fill(black)


# alt_background for something  
alt_background = pygame.Surface(screen.get_size())
alt_background = alt_background.convert()
alt_background.fill(black)

# this is for downloading images, it is the user client. 
class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

#create an opener, so we can change its user-agent
urlopen = MyOpener().open
urlretrieve = MyOpener().retrieve

# this function will handle getting weather info from the local weather website 
def weather_current(): 
   # connecting to local weather website
   connection = urllib.urlopen("http://www.wbz.com/weather")
   weather = connection.read() # reading the html of website, turning the information into a local construct
   connection.close() # closing the connecitong 

   # finding reference points to begin searching for various weather information 
   current_weather = weather.find("<!-- current conditions -->")

   # extracting various info from the references, will be -1 if the find function was unable to find anything
   if current_weather != -1 : 
      current_temp_location = weather.find("&deg;",current_weather)
      current_temp = weather[current_temp_location-2:current_temp_location]
      current_pic_start = weather.find('src=',current_weather)
      current_pic_stop = weather.find('" ',current_pic_start)
      urllib.urlretrieve(weather[current_pic_start+5:current_pic_stop], "weather.jpg") # weather img
      return current_temp 

# getting the time for the local clock 
# writting it to the screen 
# resetting the screen to display the changed time or date 
# last_min is the min displayed the last time the function was called. If the current min is different then last_min then the time will change
# last_date same thing as last_min but with the date. 
def main_screen(last_min,last_date,count): 

   current_time = str(datetime.now())
   current_date = current_time[0:10]
   current_min = current_time[10:16]

   if current_min != last_min or current_date != last_date:
   		# this handles the time 
		last_min = current_min
		last_date = current_date 
		screen.blit(main_background,(0,0))
		screen.blit(time_text.render(current_min,1,white),((width/7)-20,(height/6)+40))
		screen.blit(date_text.render(current_date,1,white),((width/7)-10,height/5))
		if count >= 15: 
			# this is handling the weather 
			c_temp = weather_current() 
			screen.blit(temp.render("the current temp is "+c_temp,1,white),(5,(height/2)))
			image_surface = pygame.image.load('weather.jpg')
			remove('weather.jpg')
			screen.blit(image_surface,(width-140,20))

		pygame.display.update()
		return last_min,last_date,count


   else: 
      return current_min,current_date,count



def main(): 
	last_min = 0 
	last_date = 0 
	count = 15
	run = True 
	while run == True: 
		[last_min,last_date,count] = main_screen(last_min,last_date,count)
		sleep(1)


main() 
