class BaseException(Exception):
    def __init__(self, message="Something went wrong"):
        self.message = message
        super().__init__(self.message)

    def _message(self):
        return self.message

class UnboundTenantError(BaseException):pass

class TenantConflict(BaseException):pass

class MaxOccurrenceError(BaseException):pass

class BlacklistedToken(BaseException):pass

class FileNotSupported(BaseException):pass

class UploadNotAllowed(BaseException):pass

class NotFoundError(BaseException):pass

class UnacceptableError(BaseException):pass