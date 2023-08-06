from .base import Op, Op0

@Op
def print_(x):
    print(x)
    return x

@Op0
def dot_(x, name, *args, **kwargs):
    try: return getattr(x, name)(*args, **kwargs)
    except: return getattr(x, name)

@Op0
def plot_(x, *args, **kwargs):
    from matplotlib import pyplot as plt
    plt.plot(x, *args, **kwargs)


def if_(x, a, b):
    if x: return a
    return b
