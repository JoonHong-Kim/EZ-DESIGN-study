from typing import Optional

from ..constants import CONTROLLER_WATERMARK, PATH_METADATA


def Controller(prefix_or_options: Optional[str] = None):
    def decorator(cls):
        default_path = "/"
        if prefix_or_options is None:
            prefix = default_path
        else:
            prefix = prefix_or_options

        setattr(cls, CONTROLLER_WATERMARK, True)
        setattr(cls, PATH_METADATA, prefix)

        return cls

    return decorator
