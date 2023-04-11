from .result import Result


class Response:
    def __init__(self, code, message, result=Result(), type=None):
        self.code = code
        self.message = message
        self.result = result
        self.type = type

    def as_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'result': self.result.as_dict(),
            'type': self.type,
        }
