import json
import urllib2

class HttpHelper():

    def send_request(self, auth_header, url):
        request = urllib2.Request(url)
        request.add_header("Authorization", auth_header)
        contents = urllib2.urlopen(request).read()
        return json.loads(contents)
