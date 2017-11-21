from BrickPi import *
from TetrixController import *
import sys
import time
import pygame



BrickPi.Address=[1,2]
BrickPi.Timeout = 100
BrickPi.SensorType [0] = 1
BrickPiSetup()
pygame.init()
screen = pygame.display.set_mode([300,300])
a=0
b=0
camb=100
camv=100
# see TetrixControllers.h for usage of initTetrixControllerSettings
initTetrixControllerSettings(BrickPi,PORT_1, 2, 0x2)
mLeftDrive=TetrixDCMotor()
initTetrixDCMotor(mLeftDrive, PORT_1, 0, 2)
mRightDrive=TetrixDCMotor()
initTetrixDCMotor(mRightDrive, PORT_1, 0, 1)
bcam = TetrixServo()
initTetrixServo(bcam, PORT_1, 1, 1)
vcam = TetrixServo()
initTetrixServo(vcam, PORT_1, 1, 2)



if BrickPiSetupSensors() : 
    sys.exit("error")


while True:
    BrickPiUpdateValues()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                a=40
                b=-40
            if event.key == pygame.K_DOWN:
                a=-40
                b=40
            if event.key == pygame.K_LEFT:
                a=-25
                b=-25
            if event.key == pygame.K_RIGHT:
                a=25
                b=25
            if event.key == pygame.K_x:
                a=0
                b=0
            if event.key == pygame.K_e:
                camb=200
            if event.key == pygame.K_q:
                camb=0
            if event.key == pygame.K_d:
                camb=100
            if event.key == pygame.K_s:
                camv=200
            if event.key == pygame.K_w:
                camv=0
            if event.key == pygame.K_a:
                camv=100

           

#        elif event.type == pygame.KEYUP:
 #           print "any"
  #          if event.key == pygame.K_UP:
   #             print "released"
    #            a=0
     #           b=0
      #      if event.key == pygame.K_DOWN:
       #         a=0
        #        b=0
         #   if event.key == pygame.K_LEFT:
          #      a=0
           #     b=0
           # if event.key == pygame.K_RIGHT:
            #    a=0
             #   b=0
    setTetrixDCMotorSpeed(BrickPi,mLeftDrive, a)
    setTetrixDCMotorSpeed(BrickPi,mRightDrive, b)
    setTetrixServoSetting(BrickPi,bcam,camb) 
    setTetrixServoSetting(BrickPi,vcam,camv)

