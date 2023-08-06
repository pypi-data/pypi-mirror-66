import traceback
from typing import Optional

# noinspection PyProtectedMember
from sentry_sdk._types import Event


def ignore_io_error(event: Event, hint: dict) -> Optional[Event]:
    if 'exc_info' in hint:
        _, exception, exc_traceback = hint['exc_info']
        if isinstance(exception, IOError):
            for _, _, failed_function, _ in traceback.extract_tb(exc_traceback):
                is_io_error = failed_function == '_get_raw_post_data'
                if is_io_error:
                    return None
    return event
