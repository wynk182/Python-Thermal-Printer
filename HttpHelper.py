import json
import urllib2
from urllib2 import HTTPError

class HttpHelper():

    def send_request(self, auth_header, url):
        request = urllib2.Request(url)
        request.add_header("Authorization", auth_header)
        contents = urllib2.urlopen(request).read()
        return json.loads(contents)

    def pingURL(self, url):
        try:
            return urllib2.urlopen(url).getcode()
        except HTTPError as e:
            return e.getcode()
