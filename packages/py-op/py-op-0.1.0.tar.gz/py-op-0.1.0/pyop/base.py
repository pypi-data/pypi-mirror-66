class O:
    """Prove that simple things do make a difference"""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self, x):
        return self.func(x, *self.args, **self.kwargs)
    def __rmatmul__(self, others):
        return [self(x) for x in others]
    def __rfloordiv__(self, other):
        return self(other)

def Op_partial(i=0):
    def wrap(fun):
        """Decorator for functions that have parameters in
        all but the i-th argument."""
        class tmp:
            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs
            def __call__(self, x):
                args, kwargs = list(self.args), self.kwargs
                args.insert(i, x)
                return fun(*args, **kwargs)
            def __rmatmul__(self, others):
                return [self.__call__(x) for x in others]
            def __rfloordiv__(self, x):
                return self.__call__(x)
        return tmp
    return wrap


def Op(fun):
    return O(fun)

Op0 = Op_partial(i=0)
Op1 = Op_partial(i=1)
Op2 = Op_partial(i=2)
Op3 = Op_partial(i=3)
