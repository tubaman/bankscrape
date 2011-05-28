import urllib, urllib2, cookielib, htmllib

__all__ = ['Scraper', 'unescape_html']

class Scraper(object):

    def __init__(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6')]
        self.opener = opener

    def get(self, url):
        req = urllib2.Request(url)
        response = self.opener.open(req)
        return response

    def post(self, url, data):
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = self.opener.open(req)
        return response


def unescape_html(s):
    s = s.replace("&nbsp;", '')
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

def test_scraper():
    b = Scraper()
    resp = b.get('http://192.168.0.2/cgi_login')
    #print resp
    resp = b.post('http://192.168.0.2/cgi_login', {'passwd': 'admin', 'post_url': 'cgi_device.'})
    #print resp
    resp = b.get('http://192.168.0.2/cgi_port')
    print resp

if __name__ == '__main__':
    test_scraper()
