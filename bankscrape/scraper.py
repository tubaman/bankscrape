try:
    from html.parser import HTMLParser
except ImportError: 
    from htmllib import HTMLParser

__all__ = ['unescape_html']

def unescape_html(s):
    s = s.replace("&nbsp;", '')
    p = HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()
