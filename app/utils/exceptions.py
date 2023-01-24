class CommonException(BaseException):
    def __init__(self, description='error', log_error_text=None):
        self.txt = description
        self.log_error_text = log_error_text if log_error_text is not None else self.txt


class ServerException(CommonException):
    status_code = 500


class ValidationError(CommonException):
    status_code = 500


class NotFoundError(CommonException):
    status_code = 404
