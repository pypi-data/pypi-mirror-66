'Checks wildcard domain names'

__version__ = '0.0.3'


import socket
from uuid import uuid1

import tldextract

ws = set()

def resolves(s):
    try:
        socket.gethostbyname(s)
    except Exception:
        return False
    return True


def gen(s):
    r = tldextract.extract(s)

    d = f'{r.domain}.{r.suffix}'
    
    yield d
    
    words = r.subdomain.split('.')
        
    for i in range(len(words)):
        prefix = '.'.join(words[-i-1:])
        yield f'{prefix}.{d}'


def resolves_random(s):
    return resolves(f'{uuid1().hex}.{s}')


def check_fresh(s):
    for c in gen(s):
        if resolves_random(c):
            return c


def check_cache(s):
    for w in ws:
        if s.endswith(f'.{w}'):
            return w


def check(s):
    w = check_cache(s)
    if w:
        return w

    w = check_fresh(s)
    if not w:
        return

    ws.add(w)
    return w
