from functools import reduce
import click


class Response:
    """Response use case

    Attributes:
        http_code (int): status code, default 404
        message (str) : message string, default 'NOT_FOUND'
        errors (list)
    """

    def __init__(
        self,
        http_code: int = 404,
        message: str = 'NOT_FOUND',
        errors: list = None
    ):
        self.http_code = http_code
        self.message = message
        self.errors = errors

    def __json__(self):
        return {
            'http_code': self.http_code,
            'message': self.message,
            'errors': self.errors,
        }


def recursive_get(d: dict, keys, default=None):
    """get recursive to dict

    Args:
        d (dict)
        keys (str|list|tuple): if is str keyA.keyB => [keyA, keyB]
        default (mixed): No required
    """
    if d is None:
        return default
    if isinstance(keys, str):
        keys = keys.split('.')
    result = reduce(lambda c, k: c.get(k, {}), keys, d)
    if default is not None and result == {}:
        return default
    return result


def response_not_found() -> tuple:
    """Function not found

    Returns:
        response (tuple): status message
    """
    return dict(message='NOT_FOUND'), 404


def response_command() -> None:
    """Function command disabled

    Returns:
        None:
    """
    click.echo('command disabled')


def response_use_case() -> Response:
    """Response use case

    Returns:
        Response:
    """
    return Response()
