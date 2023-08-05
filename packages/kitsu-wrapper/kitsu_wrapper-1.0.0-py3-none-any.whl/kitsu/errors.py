class KitsuError(Exception):
    pass


class InvalidArgument(KitsuError):
    pass


class ResponseError(KitsuError):
    __slots__ = ('code', 'reason')

    def __init__(self, *, code, reason):
        self.code = code
        self.reason = reason
        self.args = (f'Received HTTP code {code} ({reason})',)
