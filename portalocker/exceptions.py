import typing

class BaseLockException(Exception):
    LOCK_FAILED = 1

    def __init__(self, *args: typing.Any, fh: typing.Union[typing.IO, None, int]=None, **kwargs: typing.Any) -> None:
        self.fh = fh
        Exception.__init__(self, *args)

class LockException(BaseLockException):
    def __init__(self, *args: typing.Any, fh: typing.Union[typing.IO, None, int]=None, **kwargs: typing.Any) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "Failed to acquire lock"

class AlreadyLocked(LockException):
    def __init__(self, *args: typing.Any, fh: typing.Union[typing.IO, None, int]=None, **kwargs: typing.Any) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "File is already locked"

class FileToLarge(LockException):
    def __init__(self, *args: typing.Any, fh: typing.Union[typing.IO, None, int]=None, **kwargs: typing.Any) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "File is too large to lock"
