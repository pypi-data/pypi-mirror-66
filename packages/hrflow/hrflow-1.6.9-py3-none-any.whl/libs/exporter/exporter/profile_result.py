"""Classes that contains export results."""

import json


class ProfileResult(object):
    """Contains export result for a profile."""

    def __init__(self, profile):
        """Init."""
        self.profile = profile
        # if false, an error occurs for one document or on the profile itself
        # (for example cannot get documents url)
        self.is_success = True
        self.message = None
        # export result for documents
        self.docResult = []

    def set_failure(self, message):
        """Set profile status to failure."""
        self.is_success = False
        self.message = message

    def add_result_doc(self, edr):
        """Add a document result."""
        if not edr.is_success:
            self.is_success = False
            self.message = "At least document has fail."
        self.docResult.append(edr)

    def to_json(self):
        """Return a json representation of object."""
        data = {
            "no_error": self.is_success,
            "message": self.message,
            "profile_id": self.profile.id,
            "source_id": self.profile.source_id,
            "documents": []
        }
        for doc_res in self.docResult:
            doc_data = {
                "name": doc_res.document.file_name,
                "url": doc_res.document.url,
                "path": doc_res.document.export_path,
                "success": doc_res.is_success,
                "message": doc_res.message
            }
            data['documents'].append(doc_data)
        return json.dumps(data)
