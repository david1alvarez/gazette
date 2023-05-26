class RecordNotFoundException(Exception):
    def __init__(self, record):
        name = record.__class__.__name__
        message = f"Failed to find record for {name}"
        super().__init__(message)


class InvalidInputsException(Exception):
    def __init__(self, *args):
        message = "The following inputs are missing or invalid: "
        for arg in args:
            message = message + str(arg)
