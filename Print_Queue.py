import json
import qrcode
import urllib2
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

class Print_Queue():

    def send_request(auth_header, url):
        request = urllib2.Request(url)
        request.add_header("Authorization", auth_header)
        contents = urllib2.urlopen(request).read()
        return json.loads(contents)

    def print_ticket():
        print('ticket printing')

    url = "http://mossbee.ngrok.io/printer/auth.json"
    auth_header = '{"email": "michael@mossbee.com", "password":"123456ADMIN"}'
    # print(contents)
    json_data = send_request(auth_header, url)
    print(json_data)

    access_token = json_data['access_token']
    url = "http://mossbee.ngrok.io/printer/get_queue/2.json"
    auth_header = '{"access_token": "'+access_token+'"}'
    orders = send_request(auth_header, url)
    # print orders
    for val in orders:
        printer.wake()
        printer.feed(1)
        printer.justify('L')
        printer.println(val['name'])
        printer.println("Order #" + str(val['order_number']))
        printer.println(val['created'])
        printer.feed(1)
        printer.println(val['notes'])
        printer.feed(1)
        printer.println("Items")
        printer.feed(1)
        for item in val['order_items']:
            printer.println(str(item['quantity']) + ' ' + str(item['name']) + ' $' + str(item['total_price']))
            #printer.feed(1)

        #printer.println(val['order_items'])

        printer.justify('R')
        printer.println("Total: $" + val['total'])
        printer.feed(2)
        printer.justify('C')
        #print(val['order_items'])
        #print(val['name'])
        #qrcode.make("https://mossbee.ngrok.io/menus/1/orders/" + str(val['id']))#.save(str(val['order_number']) + '.bmp')
        printer.timeoutSet(1)
        printer.timeoutWait()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data("https://mossbee.ngrok.io/menus/1/orders/" + str(val['id']))
        printer.printImage(qr.make(fit=True))
        printer.justify('L')
        printer.println("--------------------------------")
        printer.feed(2)
        printer.sleep()
        #printer.qrcode.make("https://mossbee.ngrok.io/menus/1/orders/" + str(val['id']))#.save(str(val['order_number']) + '.bmp')
    # for val in json_data:
    #     qrcode.make(val['qr_url']).save(val['name'] + '.png')


    # print(json_data['qrcode'])
