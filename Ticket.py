import json
import urllib2
import qrcode
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
config = json.load(open('data.json'))

class Ticket():

    def print_ticket(self, order):
        printer.justify('L')
        printer.setSize('L')
        printer.println(order['name'])
        printer.println(" Order #" + str(order['order_number']))
        printer.setSize('M')
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
            box_size=5,
            border=2,
        )
        qr.add_data(config['baseURL'] + "/menus/"+config['menuID']+"/orders/" + str(order['id']))
        #print(qr.make(fit=True))
        qr.make(fit=True)
        #print(qr.make_image(fill_color="black", back_color="white"))
        printer.println("Scan the below QR to complete")
        printer.printImage(qr.make_image(fill_color="black", back_color="white"))
        printer.feed(1)
        printer.justify('L')
        printer.println("--------------------------------")
        printer.feed(2)
        printer.sleep()
        printer.wake()
        printer.setDefault()
