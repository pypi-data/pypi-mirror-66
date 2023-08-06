"""Upload result class."""


class Result(object):
    """Container for upload result."""

    # it's contains upload results :)
    def __init__(self):
        """Init."""
        self.is_success = False
        self.result = None
        self.file = None

    def set_failure(self, err, file):
        """Set the object with a failed upload."""
        self.is_success = False
        self.result = err
        self.file = file

    def set_success(self, resp, file):
        """Set the object with a succeed upload."""
        self.is_success = True
        self.result = resp
        self.file = file
