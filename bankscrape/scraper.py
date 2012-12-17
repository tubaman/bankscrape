import htmllib

__all__ = ['unescape_html']

def unescape_html(s):
    s = s.replace("&nbsp;", '')
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()
