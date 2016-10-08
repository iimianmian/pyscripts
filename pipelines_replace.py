#!/bin/env python3
import functools

def coroutine(f):
    @functools.wraps(f)
    def _coroutine(*args, **kwargs):
        active_coroutine = f(*args, **kwargs)
        next(active_coroutine)
        return active_coroutine
    return _coroutine

@coroutine
def replace(search, replace):
    while True:
        item = yield
        print(item.replace(search, replace))

spam_replace = replace('spam', 'bacon')
for line in open('lines.txt'):
    spam_replace.send(line.rstrip())
