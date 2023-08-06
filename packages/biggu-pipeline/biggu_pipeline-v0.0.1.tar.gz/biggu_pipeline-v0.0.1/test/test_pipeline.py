import unittest
from biggu_container import Container
from biggu_pipeline import Pipeline

class PipelineWithCustomException(Pipeline):
    @staticmethod
    def handle_exception(exception):
        return "An error has occurred"

class Foo:
    pass

class Bar:
    def handle(self, name, next):
        return "Hello " + name

class Baz:
    def handle(self, name, next, exclamation):
        signs = '!!!' if exclamation else ''
        return "Hello " + name + signs

class Biz:
    def handle(self, value, next):
        return next(value + " biz")

class Buz:
    def handle(self, value, next):
        return next(value + " buz")              

class TestPipeline(unittest.TestCase):

    @staticmethod
    def app():
        return Container()

    def test_send(self):
        pipeline = Pipeline(self.app())
        result = pipeline.send(Foo())
        self.assertIsInstance(pipeline.passable(), Foo)
        self.assertEqual(result, pipeline)

    def test_set_pipes_with_list(self):
        pipeline = Pipeline(self.app())
        foo = Foo()
        bar = Bar()
        result = pipeline.through([foo, bar])
        self.assertIsInstance(pipeline.pipes(), list)
        self.assertEqual(pipeline.pipes(), [foo, bar])
        self.assertEqual(result, pipeline)

    def test_set_pipes_with_multiple_params(self):
        pipeline = Pipeline(self.app())
        foo = Foo()
        bar = Bar()
        result = pipeline.through(foo, bar)
        self.assertIsInstance(pipeline.pipes(), list)
        self.assertEqual(pipeline.pipes(), [foo, bar])
        self.assertEqual(result, pipeline)

    def test_change_handler_method(self):
        pipeline = Pipeline(self.app())
        result = pipeline.via('custom_method')
        self.assertEqual(pipeline.method(), 'custom_method')
        self.assertEqual(result, pipeline)

    def test_prepare_destination_using_lambda(self):
        pipeline = Pipeline(self.app())
        closure = pipeline.prepare_destination(lambda passable: passable + ' through pipeline')
        result = closure("text")
        self.assertEqual(result, 'text through pipeline')

    def test_using_prepare_destination_method_as_decorator(self):
        pipeline = Pipeline(self.app())
        @pipeline.prepare_destination
        def closure(passable):
            return passable + ' through pipeline as decorator'

        result = closure("closure")
        self.assertEqual(result, 'closure through pipeline as decorator')

    def test_prepare_destination_raise_exception(self):
        pipeline = Pipeline(self.app())
        @pipeline.prepare_destination
        def closure(passable):
            return passable + ' through pipeline as decorator'  
        def raiser():
            closure(Foo)      
        self.assertRaises(Exception, raiser)

    def test_extend_for_custom_handle_execption(self):
        pipeline = PipelineWithCustomException(self.app())
        closure = pipeline.prepare_destination(lambda passable: passable + ' through pipeline')
        result = closure(Foo())
        self.assertEqual(result, 'An error has occurred')

    def test_parse_pipe_string(self):
        pipeline = Pipeline(self.app())
        self.assertEqual(pipeline.parse_pipe_string('auth:user,role'), ['auth', ['user', 'role']])
        self.assertEqual(pipeline.parse_pipe_string('auth:'), ['auth', ['']])
        self.assertEqual(pipeline.parse_pipe_string('auth'), ['auth', []])
        self.assertEqual(pipeline.parse_pipe_string(''), ['', []])

    def test_carry_method_with_class_as_pipe(self):
        pipeline = Pipeline(self.app())
        wrapper= pipeline.carry() 
        closure = wrapper([], Bar)
        result = closure("biggu")
     
        self.assertTrue(callable(wrapper))
        self.assertTrue(callable(closure))
        self.assertEqual(result, 'Hello biggu')

    def test_carry_method_with_string_as_pipe(self):
        app = self.app()
        app.instance('bar', Bar())
        pipeline = Pipeline(app)
        wrapper= pipeline.carry() 
        closure = wrapper([], 'bar')
        result = closure("biggu")
     
        self.assertTrue(callable(wrapper))
        self.assertTrue(callable(closure))
        self.assertEqual(result, 'Hello biggu')  

    def test_carry_method_with_string_and_params_as_pipe(self):
        app = self.app()
        app.instance('baz', Baz())
        pipeline = Pipeline(app)
        wrapper= pipeline.carry() 
        closure = wrapper([], 'baz:true')
        result = closure("biggu")
     
        self.assertTrue(callable(wrapper))
        self.assertTrue(callable(closure))
        self.assertEqual(result, 'Hello biggu!!!') 

    def test_carry_method_with_lambda_as_pipe(self):
        pipeline = Pipeline(self.app())
        wrapper= pipeline.carry() 
        closure = wrapper([], lambda value, next: 'Hello ' + value + " from lambda")
        result = closure("biggu")
     
        self.assertTrue(callable(wrapper))
        self.assertTrue(callable(closure))
        self.assertEqual(result, 'Hello biggu from lambda')

    def test_pipeline_flow(self):
        pipeline = Pipeline(self.app()) 
        result = pipeline.send("Hello").through([
            Biz,
            Buz
        ]).then(lambda value: value + " end")
        self.assertEqual(result, "Hello biz buz end")

