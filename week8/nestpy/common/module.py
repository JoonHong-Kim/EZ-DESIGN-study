from ..utils import validateModuleKeys


def Module(metadata: dict):
    keys = list(metadata.keys())
    validateModuleKeys(keys)

    def decorator(cls):
        for key, value in metadata.items():
            setattr(cls, key, value)

        return cls

    return decorator
