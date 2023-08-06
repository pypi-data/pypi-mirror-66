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
        if (len(self.arg_spec_args) > 1) and \
           isinstance(self.arg_spec_args[1], str) and \
           self.arg_spec_args[1].startswith('--'):
            return self.arg_spec_args[1].strip('-')
        return self.arg_spec_args[0].strip('-')


class ArgumentRunner:
    '''
    ArgumentRunner offers a decorator, parses arguments, and allows decorated functions to be ran
    '''
    
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.funcs = []
        self.parsed_args = None
        '''
            a dictionary containing parsed arguments
        '''
    
    def parse_args(self, *args, **kwargs):
        '''
        Parses arguments and returns the result as a dictionary
        '''
        parsed_args = vars(self.parser.parse_args(*args, **kwargs))
        self.parsed_args = parsed_args
        return parsed_args
    def parse(self, *args, **kwargs):
        '''
        a decorator that defines the arguments to be parsed
        and associates it with the decorated method
        '''
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
    
    def run(self, *args, **kwargs):
        '''
        Runs all decorated functions
        '''
        if self.parsed_args is None:
            self.parse_args(*args, **kwargs)
        for func_spec in self.funcs:
            if func_spec.should_run(self.parsed_args):
                arg = func_spec.get_arg(self.parsed_args)
                func_spec.func(arg)
    def add_argument(self, *args, **kwargs):
        '''
        adds an argument to be parsed without being run
        '''
        self.parser.add_argument(*args, **kwargs)

