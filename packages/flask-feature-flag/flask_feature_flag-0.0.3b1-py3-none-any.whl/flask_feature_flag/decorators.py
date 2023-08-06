import functools
from flask import current_app as app
from .utils import (
    response_command,
    response_not_found,
    response_use_case,
    recursive_get
    )


def is_enabled(response, feature):
    """Decorator to enable or disable a feature

    Args:
        response: function that returns object to return
        feature: environment variable name

    Returns:
        response: decorated function or function error
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            feature_name = recursive_get(
                app.config.get('FEATURE_FLAGS'),
                feature,
                default=False
            )
            if feature_name:
                return func(*args, **kwargs)
            return response()
        return _wrapper
    return _decorator


def command_enabled(feature: str):
    """Decorator to enable or disable a command

    Args:
        feature: environment variable name

    Returns:
        response: decorated function or response_command
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            feature_name = recursive_get(
                app.config.get('FEATURE_FLAGS'),
                feature,
                default=False
            )
            if feature_name:
                return func(*args, **kwargs)
            return response_command()
        return _wrapper
    return _decorator


def route_enabled(feature: str):
    """Decorator to enable or disable a route

    Args:
        feature: environment variable name

    Returns:
        response: decorated function or response_not_found
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            feature_name = recursive_get(
                app.config.get('FEATURE_FLAGS'),
                feature,
                default=False
            )
            if feature_name:
                return func(*args, **kwargs)
            return response_not_found()
        return _wrapper
    return _decorator


def use_case_enabled(feature: str):
    """Decorator to enable or disable a use case

    Args:
        feature: environment variable name

    Returns:
        response: decorated function or response_use_case
    """
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            feature_name = recursive_get(
                app.config.get('FEATURE_FLAGS'),
                feature,
                default=False
            )
            if feature_name:
                return func(*args, **kwargs)
            return response_use_case()
        return _wrapper
    return _decorator
