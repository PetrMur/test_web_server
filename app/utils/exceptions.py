class CommonException(BaseException):
    status_code = 500

    def __init__(self, description='error', log_error_text=None):
        self.txt = description
        self.log_error_text = log_error_text if log_error_text is not None else self.txt


class ServerException(CommonException):
    pass


class ValidationError(CommonException):
    status_code = 422


class NotFoundError(CommonException):
    status_code = 404
