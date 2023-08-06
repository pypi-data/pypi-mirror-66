from functools import wraps
import time


def callit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            _self = args[0]
        except IndexError as e:
            txt = 'Did you instantiate the object?'
            raise RuntimeError(txt) from e
        print(f'Running {_self.name}...')
        return fn(*args, **kwargs)
    return wrapper


def timeit(name):
    def real_timeit(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = fn(*args, **kwargs)
            duration = round(time.time() - t0, 2)
            print(f'{name} finished in {duration}s.')
            return result
        return wrapper
    return real_timeit
