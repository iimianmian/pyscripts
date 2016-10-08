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
def simple_coroutine():
    print('Setting up the coroutine')
    try:
        while True:
            item = yield
            print('Got item: %r' % item)
    except GeneratorExit:
        print('Normal exit')
    except Exception as e:
        print('Exception exit: %r' % e)
        raise
    finally:
        print('Any exit')
print('Creating simple coroutine')
active_coroutine = simple_coroutine()
print()
print('Sending spam')
active_coroutine.send('spam')
print()
print('Close the coroutine')
active_coroutine.close()
print()
print('Creating simple coroutine')
active_coroutine = simple_coroutine()
print()
print('Sending eggs')
active_coroutine.send('eggs')
print()
print('Throwing runtime error')
active_coroutine.throw(RuntimeError, 'Oops...')
print()
