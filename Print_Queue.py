import json
import qrcode
import urllib2
from Adafruit_Thermal import *
from Ticket import *

ticket = Ticket()

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
    #print(json_data)

    access_token = json_data['access_token']
    url = "http://mossbee.ngrok.io/printer/get_queue/2.json"
    auth_header = '{"access_token": "'+access_token+'"}'
    orders = send_request(auth_header, url)
    # print orders

    for val in orders:
        ticket.print_ticket(val)

        #printer.qrcode.make("https://mossbee.ngrok.io/menus/1/orders/" + str(val['id']))#.save(str(val['order_number']) + '.bmp')
    # for val in json_data:
    #     qrcode.make(val['qr_url']).save(val['name'] + '.png')


    # print(json_data['qrcode'])
