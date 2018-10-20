from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, socket
from PIL import Image
from Adafruit_Thermal import *
import qrcode

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

time.sleep(5)

#printer.printImage(Image.open('gfx/logo.png'), True)
printer.feed(2)

# find network ip
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]

printer.println(local_ip_address)
printer.feed(4)

# while(True):
