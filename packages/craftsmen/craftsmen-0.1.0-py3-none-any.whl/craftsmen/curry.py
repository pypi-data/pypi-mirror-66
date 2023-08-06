def _curry_builder(function, args_count, args_names, memo_args):
    def dummie(*args):
        new_args = memo_args + args
        if len(new_args) >= args_count:
            return function(*new_args)
        else:
            return _curry_builder(function, args_count, args_names, memo_args=new_args)
    return dummie

def curry(function):
    args_count = function.__code__.co_argcount
    args_names = function.__code__.co_varnames
    memo_args = ()
    return _curry_builder(
        function,
        args_count,
        args_names,
        memo_args,
    )
