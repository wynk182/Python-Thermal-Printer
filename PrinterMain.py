from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, socket
from PIL import Image
from Adafruit_Thermal import *
import qrcode
from HttpHelper import *
from Config import *

config = Config()
http = HttpHelper()
printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

time.sleep(10)

#printer.printImage(Image.open('gfx/logo.png'), True)
printer.feed(2)

#print(http.validate_connection(config.getItem('baseURL')))

# find network ip
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=2,
)
qr.add_data('http://' + local_ip_address + '/setup')
qr.make(fit=True)
printer.justify('C')
printer.println("Scan this QR code to")
printer.println("open printer configuraton")
printer.feed(1)
printer.printImage(qr.make_image(fill_color="black", back_color="white"))

printer.feed(4)
time.sleep(5)
subprocess.call(["python", "router.py"])
# while(True):
