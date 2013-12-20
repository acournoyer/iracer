#!/usr/bin/python
# This code interfaces to the i-racer rc car via bluetooth
# it accepts UDP packets as a signel byte command
# this is the use case / state machine for the device
# you can use any device to send packts
# As of right now I have a WII remote working and will soon have a web interface
# Given the UDP packet is sent localy is is almost imposible to not get it, even
# The web interface calls a local perl script that runs on the host computer not the
# users so it to should not miss.
# This is an offshoot of a USB missle launcher I worked with.
#
# Why complicate the device interface with protocol for a simple device, also
# why not make the device open to other inrefaces independent of what it was written in
# that is the real reason for using UDP

# Alex Cournoyer (AKA Old Alex)
#
# Note no device specific interfaces are called out you are free to use your own
# device as long as you can create a socket in your chosen language.


import sys
import bluetooth
import time
import socket
import time
import math
import time
import struct
from socket import *




global sock
# speeds
STOP   = 0x00
SPEED1 = 0x01
SPEED2 = 0x01
SPEED3 = 0x01
SPEED4 = 0x01
SPEED5 = 0x01
SPEED6 = 0x01
SPEED7 = 0x01
SPEED8 = 0x08
SPEED9 = 0x09
SPEED10 = 0xa
SPEED11 = 0x0b
SPEED12 = 0x0c
SPEED13 = 0x0d
SPEED14= 0x0e
SPEED15 = 0x0f

MAX_SPEED = 0x0f
MIN_SPEED = 0x01
SPEED_MASK = 0x0f

#directions F= forward R = reverse

STOP_DIR = 0x00
STRAIGHT_F = 0x10
STRAIGHT_B = 0x20
LEFT_STOP  = 0x30
RIGHT_STOP = 0x40
LEFT_F  = 0x50
RIGHT_F = 0x60
LEFT_B  = 0x70
RIGHT_B = 0x80

speed = 0
  
direction="STOP"
direction_LR = "STRAIGHT"
speed_cmd =STOP 
direction_cmd = STOP_DIR
    #speed 

# set the direction bits r/l f/b includes speed setting if stopped or moving base on speed !=0
def set_direction_cmd (cmd):
    global    direction
    global    speed
    global    direction_cmd
    global    direction_LR
    if(cmd=='L'):
        directtion_LR="LEFT"
        if(speed!=STOP):
            if(direction=="FORWARD"):
                direction_cmd=LEFT_F
            if(direction=="BACKWARD"):
                direction_cmd=LEFT_B
        else:
            direction_cmd=LEFT_STOP
    if(cmd=='R'):
        direction_LR="RIGHT"
        if(speed!=STOP):
            if(direction=="FORWARD"):
                direction_cmd=RIGHT_F
            else:
                direction_cmd=RIGHT_B
        else:
            direction_cmd=RIGHT_STOP
    if(cmd=='F'):
        directtion_LR="STRAIGHT"
        direction="FORWARD"
        if(speed!=STOP):
           direction_cmd=STRAIGHT_F
        else:
            direction_cmd=STOP_DIR
    if(cmd=='B'):
        direction_LR="STRAIGHT"
        direction="BACKWARD"
        if(speed!=STOP):
            direction_cmd=STRAIGHT_B
        else:
            direction_cmd=STOP_DIR
    if(cmd=='H'):
        #halt stop straighten out wheel or leave in position of last dir
         speed=STOP
         if(direction_LR=="RIGHT_F" or direction_LR=="RIGHT_B"):
            direction_cmd=RIGHT_STOP
         elif(direction_LR=="LEFT_F" or direction_LR=="LEFT_B"):
            direction_cmd=LEFT_STOP
         else:
            direction_cmd=STOP

            
            



# set the speed up or down 


def set_speed (cmd):
    global    speed
    #speedup
    if(cmd== 'S'):
        speed=speed+1
        if(speed>MAX_SPEED):
            speed=MAX_SPEED
    if(cmd== 's'):
        speed=speed-1
        if(speed<0):
            speed=0

        

def iracer_command (cmd):


    set_speed(cmd)
    set_direction_cmd(cmd)


    

 
def main():
    global    speed
    global    direction
    global    direction_LR
    global    speed_cmd
    global    direction_cmd
    lhost = ""
    nport = 20100
    buf  = 1

    iracer_cmd_state=0




    #setup_usb()




    # i-racer 
    # Change the number below to the Bluetooth MAC address of your i-racer
    # You get that by turning on the i-racer and and then running
    # hcitool scan

    bd_addr = "00:12:05:11:94:14"


    port = 1
    print "baddr %s ",(bd_addr,port)
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))



    addr = (lhost,nport) 
    print"socket port %d" % nport
    UDPSock = socket(AF_INET,SOCK_DGRAM)
    UDPSock.bind(addr)
    print "bind addr"
    

    while True:
            # Quite a slow refresh rate. Feel free to reduce this time (it's in seconds)
        t=time.time()
        # get one byte command easy this way no issuew with read length
        cmd,addr = UDPSock.recvfrom(buf)
        print "cmd rx: ",cmd
        old_speed=speed
        old_direction=direction
        iracer_command(cmd)
        if(old_direction != direction):
            binary_cmd= direction_cmd
            hexstring = struct.pack('B', binary_cmd)
            sock.send(hexstring)# stop first if changing directions
            print "stop 200ms when changing directions  F to B or B to F"
            print "stop cmd %#0x" %(binary_cmd)
            time.sleep(0.1)

        # the trick is to get it into a binary  byte to send
        binary_cmd=speed | direction_cmd
        hexstring = struct.pack('B', binary_cmd)
        
        print "cmd %#0x" %(binary_cmd)
        sock.send(hexstring)# stop first if changing directions
        if (cmd=='Q'):
           sock.close()
           UDPSock.close()
           sys.exit(1)
           

        


if __name__ == '__main__':
   main()

