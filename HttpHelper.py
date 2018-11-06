import json
import urllib2
from urllib2 import HTTPError
from urllib2 import URLError

class HttpHelper():

    def send_request(self, auth_header, url):
        try:
            request = urllib2.Request(url)
            request.add_header("Authorization", auth_header)
            response = json.loads(urllib2.urlopen(request).read())
            if 'error' in response:
                return None
            return response
        except Exception as e:
            return None

    def pingURL(self, url):
        try:
            return urllib2.urlopen(url).getcode()
        except HTTPError as e:
            return e.getcode()
        except URLError as e:
            return e
