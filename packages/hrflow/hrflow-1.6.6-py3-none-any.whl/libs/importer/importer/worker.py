"""Upload worker file."""

import os
import threading
from shutil import copy

from .result import Result


class Worker(threading.Thread):
    """Worker for that manage upload."""

    def __init__(self, worker_id, client, source_id, timestamp_reception, can_move_to_fail_folder, fail_folder_path):
        """Init."""
        threading.Thread.__init__(self)
        self.file_to_process = None
        self.callback = None
        self.client = client
        self.source_id = source_id
        self.timestamp_reception = timestamp_reception
        self.worker_id = worker_id
        self.can_move_to_fail_folder = can_move_to_fail_folder
        self.fail_folder_path = fail_folder_path

    def set_file(self, file, cb):
        """Add a file for next upload."""
        self.file_to_process = file
        self.callback = cb

    def process_file(self):
        """Upload file and notify supervisor."""
        res = _send_file(self.client, self.source_id, self.file_to_process, self.timestamp_reception, self.can_move_to_fail_folder, self.fail_folder_path)
        self.file_to_process = None
        self.callback(self.worker_id, res)

    def run(self):
        """Upload file until no new file is placed by callback."""
        while self.file_to_process is not None:
            self.process_file()


def _send_file(client, source_id, file_path, timestamp_reception, can_move_to_fail_folder, fail_folder_path):
    """Send a resume using riminder python api and put result in an Upload_result object."""
    res = Result()
    try:
        with open(file_path, "rb") as file:
            profile_binary = file.read()
        resp = client.profile.add_file(source_id=source_id, profile_file=profile_binary, timestamp_reception=timestamp_reception)
        if resp['code'] != 200 and resp['code'] != 201:
            res.set_failure(ValueError('Invalid response: ' + str(resp)), file_path)
            _copy_fail_folder(file_path, can_move_to_fail_folder, fail_folder_path)
        else:
            res.set_success(resp, file_path)
    except BaseException as e:
        res.set_failure(e, file_path)
        _copy_fail_folder(file_path, can_move_to_fail_folder, fail_folder_path)
    return res


def _copy_fail_folder(file_path, can_move_to_fail_folder, fail_folder_path):
    if can_move_to_fail_folder:
        copy(file_path, fail_folder_path)
