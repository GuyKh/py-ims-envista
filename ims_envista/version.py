"""Version."""


class Version:
    """Version of the package."""

    def __setattr__(self, *args: dict) -> None:
        msg = "can't modify immutable instance"
        raise TypeError(msg)

    __delattr__ = __setattr__

    def __init__(self, num: str) -> None:
        super().__setattr__("number", num)
