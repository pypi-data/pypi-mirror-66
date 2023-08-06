import argparse
from functools import wraps

class ArgSpec:
    def __init__(self, arg_spec_args, arg_spec_kwargs, func, when):
        self.arg_spec_args = arg_spec_args
        self.arg_spec_kwargs = arg_spec_kwargs
        self.func = func
        self.when = when
    def should_run(self, args):
        if self.when == 'true':
            return bool(args.get(self.key(), False))
        elif self.when is None:
            return bool(args.get(self.key(), False))
        else:
            raise ValueError('invalid when argument')
    #get the argument associated with this argument spec
    def get_arg(self, parsed_args):
        return parsed_args.get(self.key(), None)
    def key(self):
        return self.arg_spec_args[0].strip('-')


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.funcs = []
        self.parsed_args = None
    '''
        Parses arguments and returns the result as a dictionary
        takes arguments that argparse.parse_args() takes
    '''
    def parse_args(self, *args, **kwargs):
        parsed_args = vars(self.parser.parse_args(*args, **kwargs))
        self.parsed_args = parsed_args
        return parsed_args
    def parses(self, *args, **kwargs):
        when = kwargs.pop('when', None)
        self.parser.add_argument(*args, **kwargs)
        tmp = self
        def decorator(func):
            tmp.funcs += [ ArgSpec(arg_spec_args = args, arg_spec_kwargs=kwargs, func=func, when=when) ]
            @wraps(func)
            def wrapped(*args, **kwargs):
                result = func(*args, **kwargs)
            return wrapped
        return decorator
    '''
        Runs all decorated functions
        if parse_args was not called before, then it calls it with the passed arguments
    '''
    def run(*args, **kwargs):
        if self.parsed_args is None:
            self.parse_args(*args, **kwargs)
        for func_spec in self.funcs:
            if func_spec.should_run(self.parsed_args):
                arg = func_spec.get_arg(self.parsed_args)
                func_spec.func(arg)
    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

