import inspect
import functools

class Pipeline:
    def __init__(self, container):
        self._container = container
        self._passable = None
        self._pipes = []
        self._method = 'handle'

    def send(self, passable):
        self._passable = passable
        return self

    def through(self, pipes, *args):
        self._pipes = pipes if type(pipes) == list else list((pipes, *args))
        return self

    def via(self, method):
        self._method = method
        return self

    def then(self, destination):
        pipes = [*self.pipes()]
        pipes.reverse()
        pipeline = functools.reduce(self.carry(), pipes, self.prepare_destination(destination))
        return pipeline(self.passable())

    def then_return(self):
        return self.then(lambda passable: passable)
    
    def prepare_destination(self, destination):
        def wrapper(passable):
            try:
                return destination(passable)
            except Exception as exception:
                return self.handle_exception(exception)
        return wrapper

    def carry(self):
        def wrapper(stack, pipe):
            def closure(passable):
                nonlocal pipe
                try:
                    if not inspect.isclass(pipe) and callable(pipe):
                        return pipe(passable, stack)
                    elif inspect.isclass(pipe):
                        pipe = self.container().make(pipe)
                        parameters = [passable, stack]
                    elif isinstance(pipe, str):
                        [name, parameters] = self.parse_pipe_string(pipe)
                        pipe = self.container().make(name)
                        parameters = [passable, stack, *parameters]
                    else:
                        parameters = [passable, stack]

                    method = getattr(pipe, self.method(), None)
                    carry = method(*parameters) if callable(method) else pipe(*parameters)
                    return self.handle_carry(carry)
                except Exception as exception:
                    self.handle_exception(exception)
            return closure
        return wrapper

    def container(self):
        return self._container

    def pipes(self):
        return self._pipes

    def passable(self):
        return self._passable

    def method(self):
        return self._method        

    @staticmethod
    def parse_pipe_string(pipe: str):
        parts = pipe.rsplit(':', 2)
        # list right pad with empty lists
        parts.extend([[]] * (2 - len(parts)))
        [name, parameters] = parts
        if isinstance(parameters, str):
            parameters = parameters.split(',')
        return [name, parameters]

    @staticmethod
    def handle_carry(carry):
        return carry

    @staticmethod
    def handle_exception(exception):
        raise exception
