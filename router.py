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
    return render_template(
        'wifi_setup.html')

@app.route("/wifi_setup", methods=['POST'])
def submit_wifi():
    with open("form_data.txt", "w") as text_file:
        text_file.write(request.values["ssid"] + ' ' + request.values["psk"])
    #utilities.reboot

    return "Thank You!"

@app.route("/sign_in", methods=['GET'])
def sign_in():
    return render_template('user_sign_in.html')

@app.route("/sign_in", methods=['POST'])
def send_sign_in():
    #print(request.values)
    url = "http://localhost:3000/printer/auth.json"
    auth_header = '{"email": "michael@mossbee.com", "password":"123456ADMIN"}'
    # print(contents)
    json_data = http_helper.send_request(auth_header, url)
    with open("login_data.json", "w") as text_file:
        text_file.write(json_data["access_token"])
    return "recieved access token"


if __name__ == "__main__":
    app.run()
