from BrickPi import *
import pygame
from pygame.locals import * 
from TetrixController import *
import sys
 
#setting up the pygame screen and initiating pygame 
screen = pygame.display.set_mode((600,600))
pygame.font.init()

#defining colors 
BLUE = (0,0,255)
GRAY = (128,128,128)
WHITE = (255,255,255)

#defining widths and heights of squares for the visual controls. 
width1 = hieght1 = 300
width2 = hieght2 = 150
width3 = hieght3 = 80 
thickness = 2 

#this draws the rectangles for the button controls. 
pygame.draw.rect(screen,WHITE,(150,150,width1,hieght1),thickness)
pygame.draw.rect(screen,WHITE,(225,225,width2,hieght2),thickness)
pygame.draw.rect(screen,BLUE,(260,470,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(50,260,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(260,50,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(470,260,width3,hieght3),thickness)

pygame.draw.lines(screen,GRAY,False,[(150,225),(450,225)],1)
pygame.draw.lines(screen,GRAY,False,[(150,375),(450,375)],1)

#this creates the the screen and with all the rectangles 
pygame.display.update()

# this is limiting the number of commands that are accepted by the programing for pygame 
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.QUIT])

ticker = pygame.time.Clock()

# setting up brickpi 

BrickPi.Address=[1,2]
BrickPi.Timeout = 100
BrickPi.SensorType [0] = 1
BrickPiSetup()

#starting the motors in order to run them later 
# see TetrixControllers.h for usage of initTetrixControllerSettings
initTetrixControllerSettings(BrickPi,PORT_1, 2, 0x2)
mLeftDrive=TetrixDCMotor()
initTetrixDCMotor(mLeftDrive, PORT_1, 0, 1)
mRightDrive=TetrixDCMotor()
initTetrixDCMotor(mRightDrive, PORT_1, 0, 2)

baseCam = TetrixServo()
initTetrixServo(baseCam, PORT_1, 1, 1)
vertCam = TetrixServo()
initTetrixServo(vertCam, PORT_1, 1, 2)
 
# these directories are storing the values for all the differnet keystrokes for the motors. 
 # up = slow_forward , down = slow_backward, left = left, right = right, space = stop
 # w = camera_up, s = camera_down, a = camera_left, d = camera_right 
motor_key_right = {pygame.K_DOWN : -10, pygame.K_UP : 10, pygame.K_LEFT : 17, pygame.K_RIGHT : -17, pygame.K_SPACE : 0}
motor_key_left = {pygame.K_UP : 10, pygame.K_LEFT : -17, pygame.K_RIGHT : 17, pygame.K_SPACE : 0}
camera_keys_base = {pygame.K_w : 120, pygame.K_a : 60, pygame.K_d : -60}
camera_keys_vert = {pygame.K_w : 120, pygame.K_s : 200 } 

# variables that need to be globally assigned 
base_ang = 0 
while True: 
    BrickPiUpdateValues()
    for event in pygame.event.get():
        pygame.event.pump()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            [posx,posy] = pygame.mouse.get_pos()
            if posx >= 150 and posx<= 450 and posy >= 150 and posy <= 255:
                button = pygame.K_UP
            elif posx >= 150 and posx<= 450 and posy >= 375 and posy <= 450:
                button = pygame.K_DOWN
            elif posx >= 255 and posx<= 375 and posy >= 255 and posy <= 375:
                button = pygame.K_SPACE
            elif posx >= 260 and posx<= 340 and posy >= 50 and posy <= 130:
                button = pygame.K_w 
            elif posx >= 260 and posx<= 340 and posy >= 470 and posy <= 550:
                button = pygame.K_s
            elif posx >= 150 and posx<= 255 and posy >= 255 and posy <= 375:
                button = pygame.K_LEFT
            elif posx >= 375 and posx<= 450 and posy >= 255 and posy <= 375:
                button = pygame.K_RIGHT
            elif posx >= 50 and posx<= 130 and posy >= 260 and posy <= 340:
                button = pygame.K_d
            elif posx >= 470 and posx<= 550 and posy >= 260 and posy <= 340:
                button = pygame.K_a
            base_ang = camera_key_base[button] + base_ang # need this to add the base angle so that is will slowly pan 
            vert_ang = camera_key_vert[button] # this is for semetry 
            # these assign the values to the motors. 
            setTetrixDCMotorSpeed(BrickPi,mLeftDrive, motor_keys_left[button])
            setTetrixDCMotorSpeed(BrickPi,mRightDrive, motor_keys_right[button])
            setTetrixServoSetting(BrickPi,baseCam,base_ang)
            setTetrixServoSetting(BrickPi,vertCam,vert_ang)  
    elif event.type == pygame.KEYDOWN: # this will process the key press of the keybaord in realtime
            key = event.key 
            base_ang = camera_key_base[key] + base_ang # need this to add the base angle so that is will slowly pan 
            vert_ang = camera_key_vert[key] # this is for semetry 
            # these assign the values to the motors. 
            setTetrixDCMotorSpeed(BrickPi,mLeftDrive, motor_keys_left[key])
            setTetrixDCMotorSpeed(BrickPi,mRightDrive, motor_keys_right[key])
            setTetrixServoSetting(BrickPi,baseCam,base_ang)
            setTetrixServoSetting(BrickPi,vertCam,vert_ang)    
