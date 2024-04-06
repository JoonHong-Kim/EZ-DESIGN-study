from ..constants import INJECTABLE_WATERMARK


def Injectable():
    def decorator(cls):
        setattr(cls, INJECTABLE_WATERMARK, True)

        return cls

    return decorator
