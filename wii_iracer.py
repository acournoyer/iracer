#!/usr/bin/python
# This is an 
# wii_iracer
# connects to a wii remote using bluetooth (done in anothger python process)
# The cool part is that can do different actions on up and down
# It is easy to change the action via the arrays
# commands are sent via UDP (given we are local UDP is not an issue)
# the reason they are one byte is I was being lazy and did not to generate a
# a complicated command layer. The server has the state machine and interprets the commands
# into i-racer bluetooth commands (hex what a pain in python much masking
# look at iracer.py
#
# One other cool thing this python script didn't have to know anything about bluetooth

# Scoutmaster Lumpus (aka Alex Cournoyer)
# https://github.com/acournoyer/iracer
# 
# Is was based on wii_remote.py
# here is some credit where credit is due

## wii_remote_1.py
## Connect a Nintendo Wii Remote via Bluetooth
## and  read the button states in Python.
##
## Project URL :
## http://www.raspberrypi-spy.co.uk/?p=1101
##
## Author : Matt Hawkins
## Date   : 30/01/2013

# -----------------------
# Import required Python libraries
# -----------------------
import cwiid
import time
import socket






button_delay = 0.1
buttons = 0
old_buttons = 0x0fffff
nunchuk = 0
old_nunchuk = 0
nunchuk_X = 0
old_nunchuk_X = 0
def wii_delta(button_test):
   if (buttons & button_test) and ((old_buttons & button_test)!=button_test) :
       return 'UP'
   if ((buttons & button_test)!=button_test) and (old_buttons & button_test):
       return 'DOWN'

   return 'NONE'





def main ():
   global buttons
   global old_buttons
   global nunchuk
   global old_nunchuk   
   global nunchuk_X
   global old_nunchuk_X
   
   UDP_IP = "127.0.0.1"
   UDP_PORT = 20100 
   
   resp=" "
   #make list of buttons to test
   button_masks= [cwiid.BTN_LEFT, cwiid.BTN_RIGHT, cwiid.BTN_UP, cwiid.BTN_DOWN, cwiid.BTN_1, cwiid.BTN_2, cwiid.BTN_A, cwiid.BTN_B, cwiid.BTN_HOME, cwiid.BTN_MINUS, cwiid.BTN_PLUS]

   #matching list of commands to respond with
   button_mask_name=['BTN_LEFT','BTN_RIGHT','BTN_UP','BTN_DOWN','BTN_1','BTN_2','BTN_A','BTN_B','BTN_HOME','BTN_MINUS','BTN_PLUS']
   button_mask2cmd_down=['L','R','F','B','S','s','H','N','Q','N','N']
   button_mask2cmd_up = ['N','N','N','N','N','N','N','N','N','Q','N']
   # left, right forward reverse, speedup, slow down, halt,none,quit
   print 'Press 1 + 2 on your Wii Remote now ...'
   time.sleep(1)

   # Connect to the Wii Remote. If it times out
   # then quit.
   try:
       wii=cwiid.Wiimote()
   except RuntimeError:
       print "Error opening wiimote connection"
       quit()

   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
   
   print 'Wii Remote connected...\n'
   print 'Press some buttons!\n'
   print 'Press PLUS and MINUS together to disconnect and quit.\n'

   wii.rpt_mode =  cwiid.RPT_BTN | cwiid.RPT_EXT
   wii.state
   

   while True:
       old_buttons=buttons
       buttons = wii.state['buttons']

       # If Plus and Minus buttons pressed
       # together then rumble and quit.
       if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
           print '\nClosing connection ...'
           wii.rumble = 1
           time.sleep(1)
           wii.rumble = 0
           exit(wii)  


       # Check if other buttons are pressed by
       # doing a bitwise AND of the buttons number
       # and the predefined constant for that button.
       for i in range (0,len(button_masks)):
           cmd='N'   
           resp=wii_delta(button_masks[i])
           #print "buttons %#0x old buttons %#0x resp %s"%(buttons,old_buttons,resp)
           if resp == 'DOWN':
               if(button_mask2cmd_down[i]!='N'):
                   print "CMD to send on down %c for buttno %s"%(button_mask2cmd_down[i],button_mask_name[i])
                   cmd=button_mask2cmd_down[i]
           if resp == 'UP':
               if(button_mask2cmd_down[i]!='N'):
                  print "CMD to send on up %c for buttno %s"%(button_mask2cmd_up[i],button_mask_name[i])
                  cmd=button_mask2cmd_up[i]
           if(cmd!='N'):
               print 'sending cmd %s',cmd
               sock.sendto(cmd, (UDP_IP, UDP_PORT))        

       #print "old %#0x  new %#0x "%(old_buttons,buttons)
       #time.sleep(2)
 

      # if wii.state.has_key('nunchuk'):
      #     old_nunchuk=nunchuk
      #     nunchuk = wii.state['nunchuk']['buttons']
      #     if old_nunchuk!=nunchuk:
      #         print 'NUNCHUK value = %x'%nunchuk
      #     old_nunchuk_X=nunchuk_X
      #     nunchuk_X = wii.state['nunchuk']['stick'][cwiid.X]
      #     if old_nunchuk_X!=nunchuk_X:
      #         print 'NUNCHUK value = %x'%nunchuk_X




if __name__ == '__main__':
   main()

