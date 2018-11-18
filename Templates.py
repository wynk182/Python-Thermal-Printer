import json
import urllib2
import qrcode
from Adafruit_Thermal import *
from Config import *

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)
#config = json.load(open('data.json'))
config = Config()

class Templates():

    def wifi_setup(self):
        #print('test wifi')
        printer.justify('C')
        printer.println("Scan this QR code to")
        printer.println("open printer configuraton")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=2,
        )
        qr.add_data("WIFI:S:MossbeeTest;T:WPA2;P:@mossbee_;H:false;") #ip_address + '/setup')
        qr.make(fit=True)
        printer.feed(1)
        printer.printImage(qr.make_image(fill_color="black", back_color="white"))
        printer.feed(4)

    def printer_link(self):
        printer.justify('C')
        printer.println("Scan this QR code to")
        printer.println("open printer configuraton")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=2,
        )
        qr.add_data(config.getItem('baseURL') + 'printer/link/' + config.getItem('printer_token')) #ip_address + '/setup')
        qr.make(fit=True)
        printer.feed(1)
        printer.printImage(qr.make_image(fill_color="black", back_color="white"))
        printer.feed(4)

    def ticket(self, order):
        printer.setDefault()
        printer.justify('L')
        printer.println(order['name'])
        printer.println("Order #" + str(order['order_number']))
        printer.println(order['created'])
        printer.feed(1)
        printer.println(order['notes'])
        printer.feed(1)
        printer.println("Items:")
        printer.feed(1)
        for item in order['order_items']:
            printer.println(str(item['quantity']) + ' ' + str(item['name']) + ' $' + str(item['total_price']))

        printer.justify('R')
        printer.println("Total: $" + order['total'])
        printer.feed(2)
        printer.justify('C')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=2,
        )
        qr.add_data(config.getItem('baseURL') + "/menus/"+config.getItem('menuID')+"/orders/" + str(order['id']))
        #print(qr.make(fit=True))
        qr.make(fit=True)
        #print(qr.make_image(fill_color="black", back_color="white"))
        printer.println("Scan the below QR to complete")
        printer.feed(1)
        printer.printImage(qr.make_image(fill_color="black", back_color="white"))
        printer.feed(1)
        printer.justify('L')
        printer.println("--------------------------------")
        printer.feed(2)
