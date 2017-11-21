import pygame, sys 
import pygame.camera 
from pygame.locals import * 

pygame.init()
pygame.camera.init()

screen = pygame.displays.set_mode((640,480))

cam = pygame.camera.Camera("/dev/video0,(640,480)")
cam.start()

while True: 
    image = cam.get_image()
    creen.blit(image,(0,0))
    pygame.display.update()
    