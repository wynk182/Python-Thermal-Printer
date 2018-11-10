

class BootProcess():

    def CheckConnection(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
        print(local_ip_address)
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
