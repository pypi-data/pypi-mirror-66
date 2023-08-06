class DocumentResult(object):
    """Contains export result for a document."""

    def __init__(self):
        """Init."""
        self.document = None
        self.is_success = False
        self.message = None

    def set_sucess(self, document, mess):
        """Set the export to failed for the given document."""
        self.is_success = True
        self.message = mess
        self.document = document

    def set_failure(self, document, err):
        """Set the export to succes for the given document."""
        self.is_success = False
        self.message = err
        self.document = document

