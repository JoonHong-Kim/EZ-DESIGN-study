from .constants import MODULE_METADATA

INVALID_MODULE_CONFIG_MESSAGE = (
    "Invalid property '{}' passed into the @Module() decorator."
)
metadata_keys = [MODULE_METADATA["CONTROLLERS"], MODULE_METADATA["PROVIDERS"]]


def validateModuleKeys(keys: list[str]):
    def validateKey(key: str):
        if key in metadata_keys:
            return
        raise Exception(INVALID_MODULE_CONFIG_MESSAGE.format(key))

    for key in keys:
        validateKey(key)
