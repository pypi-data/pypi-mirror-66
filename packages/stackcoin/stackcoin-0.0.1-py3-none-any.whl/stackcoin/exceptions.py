class StackCoinException(Exception):
    pass


class UnexpectedState(StackCoinException):
    pass


class RequestError(StackCoinException):
    pass


class AuthenticationFailure(RequestError):
    pass


class TransferFailure(RequestError):
    pass
