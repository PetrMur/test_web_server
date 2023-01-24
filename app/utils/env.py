import os
from typing import Optional


_possible_env_vars = {}


def get_from_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get value for variable from environment

    :param name:
    :param default:
    :return:
    """

    _possible_env_vars[name] = default
    if os.environ.get(name) is not None:
        new_val = os.environ.get(name)
        return new_val
    else:
        return default
