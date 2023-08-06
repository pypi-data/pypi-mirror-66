"""Decoration Utilities."""
import time
from typing import Callable, Any

from .misc_utils import format_time, to_string, get_time_str


def timer(logger=None) -> Callable:
    """Decorate a function to log how log the function took to execute.

    Args:
        logger: logger to write to, print if None.

    Example:
        >>> from misc_utils import timer
        >>>
        >>> @get_timer(logger)
        >>> def test(a, **kwargs):
        >>>     for i in range(a):
        >>>         time.sleep(1)
        >>>
        >>> test(3, b=2, c=3)
        >>> # [INFO] 2020-01-01 15:30:00 Call ttt(3, b=2, c=3), time: 3s.

    """

    def decorator(fn: Callable) -> Callable:
        def measure_time(*args: Any, **kwargs: Any) -> Any:

            start = time.time()
            result = fn(*args, **kwargs)
            elapsed_time = time.time() - start

            args_str = to_string(args, last_comma=True) if len(args) and len(kwargs) else to_string(args)

            info = 'Called %s(%s%s), elapsed time: %.5f(s).' % (fn.__name__, args_str, to_string(kwargs), elapsed_time)
            if logger is not None:
                logger.info(info)
            else:
                print('[INFO] %s ' % get_time_str() + info)

            return result

        return measure_time

    return decorator
