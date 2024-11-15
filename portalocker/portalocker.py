import os
import typing

from . import constants
from .exceptions import LockException

LockFlags = constants.LockFlags

__all__ = ["lock", "unlock"]


class HasFileno(typing.Protocol):
    pass


LOCKER: typing.Optional[
    typing.Callable[[typing.Union[int, HasFileno], int], None]
] = None
if os.name == "nt":
    import msvcrt

    import pywintypes
    import win32con
    import win32file
    import winerror

    __overlapped = pywintypes.OVERLAPPED()

    def lock(file, flags):
        if flags & constants.LockFlags.EXCLUSIVE:
            lock_type = win32con.LOCKFILE_EXCLUSIVE_LOCK
        else:
            lock_type = 0

        if flags & constants.LockFlags.NON_BLOCKING:
            lock_type |= win32con.LOCKFILE_FAIL_IMMEDIATELY

        hfile = msvcrt.get_osfhandle(file.fileno())
        try:
            win32file.LockFileEx(hfile, lock_type, 0, -0x10000, __overlapped)
        except pywintypes.error as exc_value:
            if exc_value.winerror == winerror.ERROR_LOCK_VIOLATION:
                raise LockException(fh=file) from exc_value
            else:
                raise

    def unlock(file):
        hfile = msvcrt.get_osfhandle(file.fileno())
        try:
            win32file.UnlockFileEx(hfile, 0, -0x10000, __overlapped)
        except pywintypes.error as exc_value:
            if exc_value.winerror == winerror.ERROR_NOT_LOCKED:
                # File was not locked.
                pass
            else:
                raise

elif os.name == "posix":
    import errno
    import fcntl

    LOCKER = fcntl.flock

    def lock(file, flags):
        locking_flags = (
            fcntl.LOCK_EX
            if flags & constants.LockFlags.EXCLUSIVE
            else fcntl.LOCK_SH
        )
        if flags & constants.LockFlags.NON_BLOCKING:
            locking_flags |= fcntl.LOCK_NB
        try:
            fcntl.flock(file.fileno(), locking_flags)
        except OSError as exc_value:
            if exc_value.errno in (errno.EACCES, errno.EAGAIN):
                raise LockException(fh=file) from exc_value
            raise

    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

else:
    raise RuntimeError("PortaLocker only defined for nt and posix platforms")
