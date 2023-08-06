from .typing import Any, Callable, Enum, Optional, Sequence, Union


class GDException(Exception):
    """Base exception class for gd.py.
    This could be caught to handle any exceptions thrown from this library.
    """
    pass


class ClientException(GDException):
    """Base exception class for errors that are thrown
    when operation in :class:`Client` fails.
    """
    pass


class PaginatorException(GDException):
    """Base exception class for errors that are thrown
    when operating with :class:`Paginator` gets an error.
    """
    pass


class CommandException(GDException):
    """Base exception class for errors that are thrown
    on command parsing or invocation failure.
    """
    pass


class FailedConversion(GDException):
    """Exception that is raised when Enum converter
    fails to turn given value into requested Enum.
    """
    def __init__(self, enum: Enum, value: Any) -> None:
        self._enum = enum
        self._value = value
        message = 'Failed to convert value {!r} to enum: {!r}.'.format(value, enum)
        super().__init__(message)

    @property
    def enum(self) -> Enum:
        """:class:`enum.Enum`: Enum to which ``value`` was failed to convert."""
        return self._enum

    @property
    def value(self) -> Any:
        """`Any`: Value that was failed to be converted to ``enum``."""
        return self._value


class ParserError(GDException):
    """Exception that is raised if conversion in :class:`.XMLParser` fails."""
    pass


class EditorError(GDException):
    """Exception that is raised when converting string
    to :class:`.api.Object` or :class:`.api.Editor` failed.
    """
    pass


class HTTPError(ClientException):
    """Exception that is raised when exception
    in :class:`.utils.http.HTTPClient` occurs.
    """
    def __init__(self, exc: Exception) -> None:
        message = (
            'Failed to process HTTP request. '
            'Caused by: <{0.__class__.__name__}> ({0})'.format(exc)
        )
        self._origin = exc
        super().__init__(message)

    @property
    def origin(self) -> Exception:
        """:class:`Exception`: The original exception that was raised."""
        return self._origin


class MissingAccess(ClientException):
    """Exception that is raised when server responses with -1."""
    def __init__(self, message: Optional[str] = None) -> None:
        if message is not None:
            super().__init__(message)

        else:
            super().__init__()


class SongRestrictedForUsage(ClientException):
    """Exception that is raised when server returns -2
    when looking for a song.
    """
    def __init__(self, id: int) -> None:
        message = 'Song with id {!r} is not allowed to use.'.format(id)
        super().__init__(message)


class LoginFailure(ClientException):
    """Exception that is raised when server returns -1
    when trying to log in.
    """
    def __init__(self, login: str, password: str) -> None:
        self._login = login
        self._password = password

        message = (
            'Failed to login with parameters: '
            '<login={0!r}, password={1!r}>.'
        ).format(login, password)

        super().__init__(message)

    @property
    def login(self) -> str:
        """Username that was wrong or password did not match."""
        return self._login

    @property
    def password(self) -> str:
        """Password that login was failed with."""
        return self._password


class FailedToChange(ClientException):
    """Exception that is raised when logged in :class:`Client`
    fails to change its password or username.
    """
    def __init__(self, type: str) -> None:
        message = 'Failed to change {}. Reason: Unspecified'.format(type)  # [Future]
        super().__init__(message)


class NothingFound(ClientException):
    """Exception that is raised when server returns nothing
    that can be converted to object of name *cls_name*.
    """
    def __init__(self, cls_name: str) -> None:
        self._cls_name = cls_name
        message = 'No <{}> instances were found.'.format(cls_name)
        super().__init__(message)

    @property
    def cls_name(self) -> str:
        """Name of the class instances of which were not found."""
        return self._cls_name


class NotLoggedError(ClientException):
    """Exception that is raised when a function that requires logged in user is called
    while :class:`Client` is not logged.
    """
    def __init__(self, func_name: str) -> None:
        message = '{!r} requires client to be logged.'.format(func_name)
        super().__init__(message)


class PagesOutOfRange(PaginatorException):
    """Exception that is raised if a non-existing page
    is requested in :class:`Paginator`.
    """
    def __init__(self, page: int, info: Union[int, str]) -> None:

        if str(info).isdigit():
            message = 'Pages are out of range. Requested page: {!r}, Pages existing: {}'.format(page, info)
        else:
            message = '{} Requested page: {}'.format(info, page)

        super().__init__(message)


class CommandParseError(CommandException):
    """Exception that is raised when parsing command input has failed."""
    pass


class BadArgument(CommandException):
    """Exception that is raised when an invalid argument is passed."""
    pass


class CheckFailure(CommandException):
    """Exception that is raised when a command check has failed."""
    def __init__(self, func: Callable) -> None:
        self.check = func
        message = 'Check {} has failed.'.format(func)
        super().__init__(message)


class CheckAnyFailure(CheckFailure):
    """Exception that is raised when all checks have failed in @check_any."""
    def __init__(self, *errors: Sequence[CheckFailure]) -> None:
        self.errors = errors
        message = ('\n  ').join(('Check Any has failed. All fails:', *map(str, errors)))
        super(CommandException, self).__init__(message)
