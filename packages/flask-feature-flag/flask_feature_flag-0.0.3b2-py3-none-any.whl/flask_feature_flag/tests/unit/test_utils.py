from unittest import TestCase
from unittest.mock import patch
from ...utils import (
    response_not_found,
    response_command,
    response_use_case,
    Response
    )


class TestResponseNotFound(TestCase):
    def test_ok(self):
        result = response_not_found()
        self.assertEqual(result, ({"message": "NOT_FOUND"}, 404))


class TestResponseCommand(TestCase):
    @patch('flask_feature_flag.utils.click.echo')
    def test_ok(self, mock_echo):
        response_command()
        mock_echo.assert_called_with('command disabled')


class TestResponseUseCase(TestCase):
    def test_ok(self):
        result = response_use_case()
        self.assertIsInstance(result, Response)
