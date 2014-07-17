#!/usr/bin/env python


import httplib
import urllib

class YoClient:
    Host         = 'api.justyo.co'
    Port         = 80
    NoticeAPI    = '/yo/'
    BroadcastAPI = '/yoall/'

    Headers      = {'Cache-Control': 'no-cache',
                    'Content-Type': 'application/x-www-form-urlencoded'}

    #Proxy        =  'PROXY-HOSTNAME:PORT'
    Proxy        = None

    Token        = ''#Parse your token here
    Error        = None

    def notice(self, username):
        username = username.upper()
        param = {
            'username'  : username,
            'api_token' : self.Token,
        }

        return self._action(self.NoticeAPI, param)

    def broadcast(self):
        param = { 'api_token' : self.Token }
        return self._action(self.BroadcastAPI, param)

    def _action(self, API, param):
        param = urllib.urlencode(param)
        if self.Proxy is not None:
            conn = httplib.HTTPConnection(self.Proxy)
            API = 'http://' + self.Host + API
        else:
            conn = httplib.HTTPConnection(host=self.Host, port=self.Port)

        conn.request("POST", API, param, self.Headers)
        result = conn.getresponse()
        status = result.status / 100 == 2

        if not status:
            self.Error = result.read()
        conn.close()
        return status

if __name__ == '__main__':
    import sys
    conn = YoClient()
    if len(sys.argv) > 1:
        username = sys.argv[1]
        status = conn.notice(username)
    else:
        status = conn.broadcast()
    print conn.Error
    if (status): exit(0)
    exit(1)
