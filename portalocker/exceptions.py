import typing


class BaseLockError(Exception):
    LOCK_FAILED = 1

    def __init__(
        self,
        *args: typing.Any,
        fh: typing.Union[typing.IO, None, int] = None,
        **kwargs: typing.Any,
    ) -> None:
        self.fh = fh
        super().__init__(*args)


class LockError(BaseLockError):
    def __init__(
        self,
        *args: typing.Any,
        fh: typing.Union[typing.IO, None, int] = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "Failed to acquire lock"


class AlreadyLocked(LockError):
    def __init__(
        self,
        *args: typing.Any,
        fh: typing.Union[typing.IO, None, int] = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "File is already locked"


class FileToLarge(LockError):
    def __init__(
        self,
        *args: typing.Any,
        fh: typing.Union[typing.IO, None, int] = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, fh=fh, **kwargs)
        self.message = "File is too large to lock"
