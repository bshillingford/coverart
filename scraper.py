import lxml.html
import urllib2
import urllib
import cookielib
import re

class ScraperException(Exception):
    pass

class Page(object):
    """Represents a web page, for the purpose of web scraping"""
    def __init__(self, url, file = None, parse_html = True):

        if not file:
            file = urllib2.urlopen(url)

        self.url = url
        self.data = file.read()

        if parse_html:
            self.xml = lxml.html.fromstring(self.data)

    def xpath(self, query):
        """Executes an XPath query on the document node of the page."""
        return self.xml.xpath(query)

    def xpath_string(self, query):
        """Forces xpath to return a string, if possible."""
        return self.xml.xpath(query, smart_string=False)

    def __str__(self):
        return self.data

    def __repr__(self):
        return "Page(url = %s, node = %s)" % tuple(map(repr, [self.url, self.xml]))

class Browser(object):
    def __init__(self, cookie_policy = cookielib.DefaultCookiePolicy(), user_agent = None):
        self.current_page = None
        self.previous_page = None
        self.cookie_policy = cookie_policy
        self.cookie_jar = cookielib.CookieJar(self.cookie_policy)

        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
        if not user_agent:
            # default: Firefox 16.0.1 win32 On Windows 8 x64
            user_agent = "Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        self._opener.addheaders = [('User-Agent', user_agent)]
    
    def get(self, url, parse_html = True):
        self.previous_page = self.current_page
        self.current_page = Page(url,
                                 file = self._opener.open(url),
                                 parse_html = parse_html)
        
    def post(self, url, data, parse_html = True):
        self.previous_page = self.current_page

        if type(data) is dict or (type(data) is list and len(data) > 0 and len(data[0]) == 2):
            data = urllib.urlencode(data)
        self.current_page = Page(url,
                                 file = self._opener.open(url, data),
                                 parse_html = parse_html)
