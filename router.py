from flask import Flask, flash, redirect, render_template, request, session, abort
from os_utilities import *
from HttpHelper import *
from Config import *

config = Config()
http_helper = HttpHelper()
utilities = os_utilities()

app = Flask(__name__)

@app.route("/")
def index():
    return "WTF"

@app.route("/wifi_setup", methods=['GET'])
def wifi_setup():
    #list = utilities.scan_networks
    return render_template('wifi_setup.html')

@app.route("/wifi_setup", methods=['POST'])
def submit_wifi():
    #print(request.form.get('ssid'))# request.form.get('psk'))
    #print(request.form)
    config.updateItem('ssid', request.form.get('ssid'))
    config.updateItem('psk', request.form.get('psk'))
    config.writeWifiConfig()
    #return render_template('thank_you.html')
    return "Thanks!"

@app.route("/setup", methods=['GET'])
def sign_in():
    return render_template('user_sign_in.html', status='Load')

@app.route("/setup", methods=['POST'])
def send_sign_in():
    if(request.form.get('location') == 'sign_in'):
        url = config.getItem('baseURL') + config.epAuthorize
        auth_header = '{"email": "'+request.form.get("email")+'", "password":"'+request.form.get("password")+'"}'
        json_data = http_helper.send_request(auth_header, url)
        if json_data:
            config.updateItem('access_token', json_data["access_token"])
        else:
            return render_template('user_sign_in.html', status='Error')
        #url = config.getItem('baseURL') + "printer/menu_options"
        #auth_header = '{"access_token":"'+json_data["access_token"]+'"}'
        #menu_options = http_helper.send_request(auth_header, url)
        #return render_template('menus.html', options=menu_options)

    elif(request.form.get('location') == 'menu_save'):
        config.updateItem('selectedMenu', request.form.get('menu'))
        return "Thanks"
    else:
        return "thanks"

@app.route("/menus", methods=['GET'])
def menu():
    url = config.getItem('baseURL') + config.epMenus
    auth_header = '{"access_token":"'+config.getItem('access_token')+'"}'
    menu_options = http_helper.send_request(auth_header, url)
    return render_template('menus.html', options=menu_options)

@app.route("/menus", methods=['POST'])
def set_menu():
    config.updateItem('selectedMenu', request.form.get('menu'))
    return "Thanks"

if __name__ == "__main__":
    app.run()
