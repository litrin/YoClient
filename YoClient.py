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

    Token        = '' #Parse your token here
    Error        = None

    link         = None

    def notice(self, username, link=None):
        username = username.upper()
        self.setLink(link)
        param = {
            'username'  : username,
            'api_token' : self.Token,
        }

        if self.link is not None:
            param['link'] = self.link

        return self._action(self.NoticeAPI, param)

    def broadcast(self, link=None):
        self.setLink(link)

        param = { 'api_token' : self.Token }

        if self.link is not None:
            param['link'] = self.link

        return self._action(self.BroadcastAPI, param)

    def setLink(self, link):
        if link is not None:
            self.link = link

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


class IWantYo(YoClient):

    _imageGenratorUrl = 'http://www.hetemeel.com/unclesamshow.php'

    def setLink(self, text):
        YoClient.setLink(self, self._genrateUrl(text))

    def _genrateUrl(self, text):
        return "%s?%s" % (self._imageGenratorUrl, urllib.urlencode({'text' : text}))

    setText = setLink

if __name__ == '__main__':
    import sys
    conn = IWantYo()
    link = 'https://github.com/litrin/YoClient'

    if len(sys.argv) > 1:
        username = sys.argv[1]
        status = conn.notice(username, link)
    else:
        status = conn.broadcast(link)

    if (status): exit(0)
    exit(1)
