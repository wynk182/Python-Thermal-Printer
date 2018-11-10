from __future__ import print_function
#import RPi.GPIO as GPIO
import subprocess, time, socket
from PIL import Image
#from Adafruit_Thermal import *
import qrcode
from HttpHelper import *
from Config import *
from Templates import *
from BootProcess import *
import random
import string

template = Templates()
config = Config()
http = HttpHelper()
boot = BootProcess()
#printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

time.sleep(5)
subprocess.call(["sudo","service", "hostapd", "stop"])
subprocess.call(["sudo","service", "dnsmasq", "stop"])
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
        subprocess.call(["sudo","cp","interfaces.normal","/etc/network/interfaces"])
        subprocess.call(["sudo","service","networking","restart"])
        time.sleep(5)
        if http.pingURL(config.getItem("baseURL")) == 200:
            subprocess.call(["git","pull"])
            boot.CheckConnection()
        #subprocess.call(["sudo","reboot"])
    #print("No Wifi config, print wifi setup link!")
else:
    if http.pingURL(config.getItem("baseURL")) == 200:
        subprocess.call(["git","pull"])
        boot.CheckConnection()
        # self.printLoginURL(local_ip_address)
        # template.printer_link()
    else:
        print("Connection Error, print wifi setup link")
        # self.printWifiURL()
        subprocess.call(["sudo","cp","interfaces.captive","/etc/network/interfaces"])
        subprocess.call(["sudo","service","networking","restart"])
        subprocess.call(["sudo","service", "hostapd", "start"])
        subprocess.call(["sudo","service", "dnsmasq", "start"])
        subprocess.call(["sudo","service", "hostapd", "stop"])
        subprocess.call(["sudo","nodogsplash"])
        template.wifi_setup()

subprocess.call(["python", "router.py"])
