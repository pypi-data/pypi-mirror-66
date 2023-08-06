from toolz import itertoolz
from functools import reduce
from .base import Op, Op0, Op1

def isiterable(x):
    try: len(x)
    except: return False
    return True
@Op
def car_(x):
    assert isiterable(x)
    if len(x) == 0: return None
    return x[0]
@Op
def cdr_(x):
    assert isiterable(x)
    if len(x) == 0: return ()
    return x[1:]
@Op
def cadr_(x):
    return x // cdr // car
@Op
def caar_(x):
    return x // car // car
@Op
def cddr_(x):
    return x // cdr // cdr
@Op
def cdar_(x):
    return x // car // cdr
@Op
def caaar_(x):
    return x // car // caar
@Op
def caadr_(x):
    return x // cdr // caar
@Op
def cadar_(x):
    return x // car // cadr
@Op
def caddr_(x):
    return x // cdr // cadr
@Op
def cdaar_(x):
    return x // car // cdar
@Op
def last_(x):
    return x[-1]
@Op
def first_(x):
    return x // car
@Op1
def filter_(func, x):
    return filter(func, x)
@Op
def list_(x):
    return list(x)
@Op
def enumerate_(x):
    return enumerate(x)
@Op
def len_(x):
    return len(x)
@Op0
def reduce_(x, func):
    return reduce(func, x)
@Op0
def partition_(x, n):
    return itertoolz.partition(n, x)
@Op0
def take_(x, n):
    return itertoolz.take(n, x)
@Op0
def remove_(x, func):
    return itertoolz.remove(func, x)
@Op0
def topk_(x, k):
    return itertoolz.topk(k, x)
@Op
def unique_(x):
    return itertoolz.unique(x)
@Op0
def plunk_(x, i):
    return itertoolz.plunk(i, x)
@Op0
def repeat_(x, n):
    return [x for x in range(n)]
