import pygame 
from time import sleep
from datetime import datetime

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
screen = pygame.display.set_mode((300,300))
pygame.display.set_caption('test')

# background screen for the time 
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

# weather screen 
weather_screen = pygame.Surface(screen.get_size())

# this is creating a font surface to be render to another surface
time_text = pygame.font.Font(None,40)
date_text = pygame.font.Font(None,30)
weather_button = pygame.font.Font(None,20)
email_button = pygame.font.Font(None,20)

# drawing the buttons 
pygame.draw.rect(background,red,(50,200,100,50))
background.blit(weather_button.render('Weather',1,white),(75,220))
pygame.draw.rect(background,blue,(160,200,100,50))
background.blit(email_button.render("Email",1,white),(190,220))


# blit(surface,(x,y)) this will draw a surface on to another surface
# font.render("text",1,(r,g,b)) # this will draw text to the surface created by the font. 
x = 150
y = 150

def time_date(current_min,current_date): 
	last_min = current_min
	last_date = current_date 
	screen.blit(background,(0,0))
	screen.blit(time_text.render(current_min,1,white),(x-30,y))
	screen.blit(date_text.render(current_date,1,white),(x-40,y-50))
	pygame.display.update()
	return last_min,last_date

def weather(): 

def main():
	time_screen = 1
	last_min = 0 
	last_date = 0 
	while True: 
   		current_time = str(datetime.now())
   		current_date = current_time[0:10]
   		current_min = current_time[10:16]
   		if current_min != last_min or current_min != last_date or time_screen = 1:
   			time_screen = 0  
   			[last_min,last_date] =time_date(current_min,current_date)
   		for event in pygame.event.get():
   			pygame.event.pump()
   			if event.type == pygame.MOUSEBUTTONDOWN:
   				[posx,posy] = pygame.mouse.get_pos() 
   				if posx >= 50 and posx <= 150 and posy >= 200 and posy <= 250: 
   					print "weather"
   				elif posx >= 160 and posx <= 260 and posy >= 200 and posy <= 250: 
   					print "email"   			
   	sleep(2)


main()