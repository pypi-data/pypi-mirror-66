from flask import current_app as app
from .utils import recursive_get


def flag_on(key: str) -> bool:
    """Enable or disable a feature

    Example:
    ::
        if flag_on('MY_KEY'):
            pass

    Args:
        key (str):

    Returns:
        bool:
    """
    return recursive_get(app.config, f'FEATURE_FLAGS.{key}', False)
