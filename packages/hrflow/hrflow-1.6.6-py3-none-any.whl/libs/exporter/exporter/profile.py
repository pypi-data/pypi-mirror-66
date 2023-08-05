"""Class that contain useful profile datas."""
from .api_utils import exec_api_call
from .profile_document import ProfileDocument


class Profile(object):
    """Contains profile datas."""

    def __init__(self, profile_id, source_id):
        """Init."""
        self.id = profile_id
        self.source_id = source_id
        self.documents = []

    def fill_documents_from_api(self, client):
        """Get document files data from api."""
        # It gets the name and the url.
        resp, err = exec_api_call(lambda: client.profile.attachment.list(source_id=self.source_id, profile_id=self.id))
        if err is not None:
            err = "Cannot get document: {}".format(err)
            return err
        for doc in resp['data']:
            d = ProfileDocument(self.id + "_" + doc['type'] + "." + doc['extension'], url=doc['public_url'])
            self.documents.append(d)
        # Also for parsing json
        resp, err = exec_api_call(lambda: client.profile.parsing.get(source_id=self.source_id, profile_id=self.id))
        if err is not None:
            err = "Cannot get parsing data: {}".format(err)
            return err
        d = ProfileDocument(self.id + '.json', data=resp['data'])
        self.documents.append(d)
        return None
