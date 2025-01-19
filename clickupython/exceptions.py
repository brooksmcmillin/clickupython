from typing import Optional


class ClickupClientError(Exception):
    def __init__(self, error_message: str, status_code: Optional[str | int] = None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self) -> str:
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message
