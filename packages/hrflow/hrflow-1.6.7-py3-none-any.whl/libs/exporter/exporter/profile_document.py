

class ProfileDocument(object):
    """Contains data for a profile document."""

    def __init__(self, name, url=None, data=None):
        """Init."""
        self.file_name = name
        self.url = url
        self.data = data
        self.export_path = None
        self.export_jsons_path = None

