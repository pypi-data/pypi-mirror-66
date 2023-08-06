from unittest import TestCase
import click
from flask import Flask
from ...utils import (
    response_not_found,
    Response
    )
from ...decorators import (
    is_enabled,
    command_enabled,
    route_enabled,
    use_case_enabled
)


class TestIsEnabled(TestCase):

    def test_enable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_HI': True}

        with self._app.app_context():
            @is_enabled(response_not_found, 'ENV_HI')
            def hi(name):
                return {'data': name, 'message': 'ok'}

            result = hi('success')

            self.assertEqual(result, {'data': 'success', 'message': 'ok'})
            self.assertEqual(hi.__name__, 'hi')

    def test_disable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_HI': False}

        with self._app.app_context():
            @is_enabled(response_not_found, 'ENV_HI')
            def hi(name):
                pass

            result = hi('success')

            self.assertEqual(result, ({'message': 'NOT_FOUND'}, 404))
            self.assertEqual(hi.__name__, 'hi')


class TestCommandEnabled(TestCase):
    def test_enable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_RUN_COMMAND': True}

        with self._app.app_context():

            @command_enabled('ENV_RUN_COMMAND')
            def run_command():
                click.echo('I am command')

            result = run_command()

            self.assertIsNone(result)
            self.assertEqual(run_command.__name__, 'run_command')


class TestRouteEnabled(TestCase):
    def test_enable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_RUN_ROUTE': True}

        with self._app.app_context():

            @route_enabled('ENV_RUN_ROUTE')
            def run_route():
                return dict(message='OK'), 200

            result = run_route()

            self.assertEqual(result, ({'message': 'OK'}, 200))
            self.assertEqual(run_route.__name__, 'run_route')

    def test_disable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_RUN_ROUTE': False}

        with self._app.app_context():

            @route_enabled('ENV_RUN_ROUTE')
            def run_route():
                pass

            result = run_route()
            self.assertEqual(result, ({'message': 'NOT_FOUND'}, 404))
            self.assertEqual(run_route.__name__, 'run_route')


class TestUseCaseEnabled(TestCase):
    def test_enable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_RUN_USE_CASE': True}

        with self._app.app_context():

            @use_case_enabled('ENV_RUN_USE_CASE')
            def run_use_case():
                return Response(
                    http_code=200,
                    message='OK'
                )

            result = run_use_case()

            self.assertIsInstance(result, Response)
            self.assertEqual(result.http_code, 200)
            self.assertEqual(run_use_case.__name__, 'run_use_case')

    def test_disable(self):
        self._app = Flask(__name__)
        self._app.config['FEATURE_FLAGS'] = {'ENV_RUN_USE_CASE': False}

        with self._app.app_context():

            @use_case_enabled('ENV_RUN_USE_CASE')
            def run_use_case():
                pass

            result = run_use_case()

            self.assertIsInstance(result, Response)
            self.assertEqual(result.http_code, 404)
            self.assertEqual(run_use_case.__name__, 'run_use_case')
