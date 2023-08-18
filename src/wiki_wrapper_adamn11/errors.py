class NoDataException(Exception):
    "Raised when there are no data or the data has not been loaded yet"
    pass


class ThrottlingException(Exception):
    "Raised when the client has made too many requests and it is being throttled"
    pass
