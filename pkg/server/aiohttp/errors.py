class ApiError(Exception):
    def __init__(self, message):
        super().__init__(message)

    code = 500


class ErrNotFount(ApiError):
    code = 404


class ErrForbidden(ApiError):
    code = 400
