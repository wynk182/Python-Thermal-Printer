from flask import Flask, flash, redirect, render_template, request, session, abort
from os_utilities import *
from HttpHelper import *

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
    print(request.form.get('ssid'))# request.form.get('psk'))
    print(request.form)
    with open("form_data.txt", "w") as text_file:
        text_file.write(request.form.get('ssid') + ' ' + request.form.get('psk'))
    return render_template('thank_you.html')

@app.route("/setup", methods=['GET'])
def sign_in():
    return render_template('user_sign_in.html')

@app.route("/setup", methods=['POST'])
def send_sign_in():
    if(request.form.get('location') == 'sign_in'):
        #print(request.values)
        url = "http://localhost:3000/printer/auth.json"
        auth_header = '{"email": "'+request.form.get("email")+'", "password":"'+request.form.get("password")+'"}'
        # print(contents)
        json_data = http_helper.send_request(auth_header, url)
        with open("login_data.txt", "w") as text_file:
            text_file.write(json_data["access_token"])
        url = "http://localhost:3000/printer/menu_options"
        auth_header = '{"access_token":"'+json_data["access_token"]+'"}'
        menu_options = http_helper.send_request(auth_header, url)
        return render_template('menus.html', options=menu_options)
    else:
        return "thanks"


if __name__ == "__main__":
    app.run()
