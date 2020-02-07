
def curry(f):
    """Turn a function that accepts a list of arguments to a function that
    accepts the respective arguments. Only applies to non-keyworded arguments."""
    def curried(*args, **kwargs): return f(args, **kwargs)
    return curried


def uncurry(f):
    """Turns a function that accepts arguments into a functions that accepts
    these arguments as list. Applies only to non-keyworded arguments."""
    def uncurried(arg, **kwargs): return f(*arg, **kwargs)
    return uncurried
