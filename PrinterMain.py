from __future__ import print_function
#import RPi.GPIO as GPIO
import subprocess, time, socket
from PIL import Image
#from Adafruit_Thermal import *
import qrcode
from HttpHelper import *
from Config import *
from Templates import *
import random
import string

template = Templates()
config = Config()
http = HttpHelper()
#printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

time.sleep(10)

#printer.printImage(Image.open('gfx/logo.png'), True)
#printer.feed(2)
if not config.validateItem('printer_token'):
    random = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    if not open('secret_printer_key'):
        with open('secret_printer_key', 'w') as f:
            f.write(random)
    else:
        with open('secret_printer_key', 'r') as f:
            random = f.readline()
    config.updateItem('printer_token', random)

#print(http.validate_connection(config.getItem('baseURL')))

# find network ip
if config.loadWifiConfig() is None:
    if config.validateItem('ssid'):
        config.writeWifiConfig()
    #print("No Wifi config, print wifi setup link!")
else:
    if http.pingURL(config.getItem("baseURL")):
        print("Connected!")
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
        #print(local_ip_address)
        config.updateItem('IP', local_ip_address)
        if config.validateItem('access_token'):
            url = config.getItem('baseURL') + config.epValidate
            auth_header = '{"access_token":"'+config.getItem('access_token')+'"}'
            response = http.send_request(auth_header,url)
            if response:
                print('valid')
            else:
                #print('invalid')
                template.printer_link()
        # self.printLoginURL(local_ip_address)
        # template.printer_link()
    else:
        print("Connection Error, print wifi setup link")
        # self.printWifiURL()
        template.wifi_setup()

subprocess.call(["python", "router.py"])
