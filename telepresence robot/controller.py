from BrickPi import *
import pygame
from pygame.locals import * 
from TetrixController import *
import sys
 
#setting up the pygame screen and initiating pygame 
screen = pygame.display.set_mode((600,600))
pygame.font.init()

BLUE = (0,0,255)
GRAY = (128,128,128)
WHITE = (255,255,255)

width1 = hieght1 = 300
width2 = hieght2 = 150
width3 = hieght3 = 80 
thickness = 2 

pygame.draw.rect(screen,WHITE,(150,150,width1,hieght1),thickness)
pygame.draw.rect(screen,WHITE,(225,225,width2,hieght2),thickness)
pygame.draw.rect(screen,BLUE,(260,470,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(50,260,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(260,50,width3,hieght3),thickness)
pygame.draw.rect(screen,BLUE,(470,260,width3,hieght3),thickness)

pygame.draw.lines(screen,GRAY,False,[(150,225),(450,225)],1)
pygame.draw.lines(screen,GRAY,False,[(150,375),(450,375)],1)

pygame.display.update()

pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN])

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
 
# Setting variables

L_motor = 'none'
R_motor = 'none'
Cam_h = 'none'
Cam_v = 'none'
L_last = "nothing"
R_last = 'nothing'
slow_forward = 10 
forward = 35
fast_forward = 50 
slow_back = -10 
back = -35 
fast_back = -50 
L_left = -17
R_left = 17 
L_right = 17 
R_right = -17
STOP = 0 
Cam_h_front = 'cam_h_front'
Cam_v_front = 'cam_v_front'
Cam_down = 'cam_down'
Cam_left = 'cam_left'
Cam_right = 'cam_right'
base_ang = 120
vert_ang = 120
count = "" 
next_up = ""
f_or_back = ""
time = 0 

def move_mouse(posx, posy):
    if posx >= 150 and posx<= 450 and posy >= 150 and posy <= 255:
        return (slow_forward, slow_forward, 'none', 'none')
    elif posx >= 150 and posx<= 450 and posy >= 375 and posy <= 450:
        return (slow_back, slow_back, 'none', 'none')
    elif posx >= 255 and posx<= 375 and posy >= 255 and posy <= 375:
        return (STOP, STOP, 'none', 'none')
    elif posx >= 260 and posx<= 340 and posy >= 50 and posy <= 130:
        return ('none', 'none', Cam_v_front, Cam_h_front)
    elif posx >= 260 and posx<= 340 and posy >= 470 and posy <= 550:
        return ('none', 'none', Cam_down, 'none')
    elif posx >= 150 and posx<= 255 and posy >= 255 and posy <= 375:
        return (L_left, R_left, 'none', 'none')
    elif posx >= 375 and posx<= 450 and posy >= 255 and posy <= 375:
        return (L_right, R_right, 'none', 'none')
    elif posx >= 50 and posx<= 130 and posy >= 260 and posy <= 340:
        return ('none', 'none', 'none', Cam_right)
    elif posx >= 470 and posx<= 550 and posy >= 260 and posy <= 340:
        return ('none', 'none', 'none', Cam_left)
    else: 
        return ('none','none','none','none')

def move_key(key): 
    if event.key == pygame.K_UP :
        return (slow_forward, slow_forward, 'none', 'none')
    elif event.key == pygame.K_DOWN :
        return (slow_back, slow_back, 'none', 'none')
    elif event.key == pygame.K_LEFT :
        return (L_left, R_left, 'none', 'none')
    elif event.key == pygame.K_RIGHT : 
        return (L_right, R_right, 'none', 'none')
    elif event.key == pygame.K_SPACE :
        return (STOP, STOP, 'none', 'none')
    elif event.key == pygame.K_w :
        return ('none', 'none', Cam_v_front, Cam_h_front)
    elif event.key == pygame.K_s :
        return ('none', 'none', Cam_down, 'none')
    elif event.key == pygame.K_a :
        return ('none', 'none', 'none', Cam_left)
    elif event.key == pygame.K_d :
        return ('none', 'none', 'none', Cam_right)
    else: 
        return ('none', 'none', 'none','none')

def last_time_controll(L_M, R_M, V_M, H_M):
    global time 
    global f_or_back
    if L_M == slow_forward and R_M == slow_forward and V_M == 'none' and H_M == 'none':
        time = 0 
        Drive_Motors(L_M, R_M)
        f_or_back = 'slow_forward'
    elif L_M == slow_back and R_M == slow_back and V_M == 'none' and H_M == 'none':
        time = 0 
        Drive_Motors(L_M, R_M) 
        f_or_back = 'slow_back'
    elif L_M != R_M and V_M == 'none' and H_M == 'none' :
        Drive_Motors(L_M, R_M)
        f_or_back = 'nothing'
    elif L_M == STOP and V_M == STOP :
        Drive_Motors(L_M, R_M)
        f_or_back = 'nothing'
    elif L_M == 'none' and R_M == 'none' : 
        Cam_Motors(V_M, H_M) 
    elif L_M == STOP and R_M == STOP: 
        Drive_Motors(L_M, R_M)
        f_or_back = 'nothing'

def Drive_Motors(LM, RM):
    print LM, RM 
    setTetrixDCMotorSpeed(BrickPi,mLeftDrive, LM)
    setTetrixDCMotorSpeed(BrickPi,mRightDrive, RM)

def Cam_Motors(VM, HM):
    global base_ang
    global vert_ang
    if VM == Cam_v_front and HM == Cam_h_front: 
        print "camera front and center " 
        base_ang = 120 
        vert_ang = 120 
    elif VM == Cam_down and HM == 'none':
        print "camera is going down" 
        vert_ang = 200
    elif HM == Cam_left and VM == 'none': 
        print "camera is going left" 
        base_ang = base_ang -60
    elif HM == Cam_right and VM == 'none' : 
        print " going to the right"
        base_ang = base_ang +60
    setTetrixServoSetting(BrickPi,baseCam,base_ang)
    setTetrixServoSetting(BrickPi,vertCam,vert_ang)

# taking care of the camera initial set up
setTetrixServoSetting(BrickPi,baseCam,base_ang)
setTetrixServoSetting(BrickPi,vertCam,vert_ang)

#cheking to see if the brickpi is connected
if BrickPiSetupSensors() :
    sys.exit("error")

# the while loop to run the program
while True: 
     for event in pygame.event.get():
         pygame.event.pump()
         if event.type == pygame.MOUSEBUTTONDOWN: 
             [posx,posy] = pygame.mouse.get_pos()
             [L_motor, R_motor, Cam_v, Cam_h] = move_mouse(posx,posy)
             last_time_controll(L_motor, R_motor, Cam_v, Cam_h)
         elif event.type == pygame.KEYDOWN: 
             key = event.key 
             [L_motor, R_motor, Cam_v, Cam_h] = move_key(key)
             last_time_controll(L_motor, R_motor, Cam_v, Cam_h)
         elif event.type == QUIT : 
             break
#         BrickPiUpdateValues()

 
     else:
         time += ticker.get_time()
         if time >= 4500000000 and time <= 8000000000 :
             if f_or_back == 'slow_forward':
                 f_or_back = 'forward'
                 L_motor = R_motor = forward 
                 Drive_Motors(L_motor, R_motor)
             elif f_or_back == 'slow_back':
                 f_or_back = 'back'
                 L_motor = R_motor = back
                 Drive_Motors(L_motor, R_motor)

         if time >= 17000000000 and time <= 19000000000 : 
             if f_or_back == 'forward':
                 f_or_back = 'fast_forward'
                 L_motor = R_motor = fast_forward 
                 Drive_Motors(L_motor, R_motor)
             elif f_or_back == 'back':
                 f_or_back = 'fast_back'
                 L_motor = R_motor = fast_back
                 Drive_Motors(L_motor, R_motor)
         if time >= 360000000000:
             time = 20000000000
         pygame.time.delay(500)
      
     BrickPiUpdateValues()
