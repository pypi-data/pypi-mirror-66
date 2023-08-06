"""Upload supervisor class."""
# Upload supervisor is the class that orchestrate all the upload process
# Also, it's resposible for all the pretty outputs

import errno
import json
import os
import random
import sys
import threading
import time

from .worker import Worker

VALID_EXTENSIONS = ['.pdf', '.PNG', '.png', '.jpg', '.jpeg', '.bmp', '.doc', '.docx', '.rtf', '.dotx', '.odt', '.odp', '.ppt', '.pptx', '.rtf', '.msg']
INVALID_FILENAME = ['.', '..']
SIZE_PROGRESS_BAR = 50

VERBOSE_LEVEL_SILENT = 'silent'
VERBOSE_LEVEL_NORMAL = 'normal'
VERBOSE_LEVEL_VERBOSE = 'verbose'

FOLDER_NAME_FAILED_RESUMES = "failed-resumes"


def is_valid_extension(file_path):
    """Check if an file extension is valid."""
    ext = os.path.splitext(file_path)[1]
    if not ext:
        return False
    return ext in VALID_EXTENSIONS


def is_valid_filename(file_path):
    """Check if a filename is valid."""
    name = os.path.basename(file_path)
    return name not in INVALID_FILENAME


def get_files_from_dir(dir_path, is_recurcive):
    """Get all filepath from a given directory."""
    file_res = []
    files_path = os.listdir(dir_path)

    for file_path in files_path:
        # true path is the path from the dir_path to the selected file
        true_path = os.path.join(dir_path, file_path)

        # Get file recursivly in subdirectories if asked
        if os.path.isdir(true_path) and is_recurcive:
            if is_valid_filename(true_path):
                file_res += get_files_from_dir(true_path, is_recurcive)
            continue
        if is_valid_extension(true_path):
            file_res.append(true_path)
    return file_res


def get_filepaths_to_send(paths, is_recurcive):
    """Get all file path from a list of file and dirs."""
    res = []
    for fpath in paths:
        if not is_valid_filename(fpath):
            print('Not a valid filename: \n'.format(fpath))
            continue
        if os.path.isdir(fpath):
            res += get_files_from_dir(fpath, is_recurcive)
            continue
        if not is_valid_extension(fpath):
            print('Not a valid extension: \n'.format(fpath))
            continue
        res.append(fpath)
    return res


class Supervisor(object):
    """Manage upload, worker, and logging."""

    def __init__(self, client, source_id, target, timestamp_reception=None, is_recurcive=True, silent=False,
                 verbose=True, sleep=1, n_worker=3, logfile=None):
        """
        Init using command args datas and files to upload.
        """
        self.client = client
        self.target = get_filepaths_to_send(target, is_recurcive)
        self.is_recurcive = is_recurcive
        self.source_id = source_id
        self.sleep = int(sleep)
        self.v_level = VERBOSE_LEVEL_NORMAL
        if silent:
            self.v_level = VERBOSE_LEVEL_SILENT
        if verbose:
            self.v_level = VERBOSE_LEVEL_VERBOSE
        self.n_worker = n_worker
        self.timestamp_reception = timestamp_reception
        self.workers = {}
        self.lock_worker = threading.Lock()
        self.lock_printer = threading.Lock()
        self.results = []
        self.n_failed = 0
        self.n_file_to_send = len(self.target)
        self.logfile = None
        if logfile is not None:
            self.logfile = open(logfile, mode='w')
        self.can_move_to_fail_folder, self.fail_folder_path = self._create_failed_folder()

    def _set_worker_file(self, workerID):
        if len(self.target) == 0:
            return
        # pop a file for the stack and give it to a worker (to avoid upload duplication)
        self.workers[workerID].set_file(self.target.pop(), self.worker_callback)
        time.sleep(self.sleep)
        
    def _init_workers(self):
        for i in range(self.n_worker):
            self.workers[i] = Worker(i, self.client, self.source_id, self.timestamp_reception, self.can_move_to_fail_folder, self.fail_folder_path)
            # Give a file before start a worker to avoid the workers to die instantly
            self._set_worker_file(i)

    def worker_callback(self, workerID, file_result):
        """Callback function used by workers to notify when file has been sended."""
        self.lock_worker.acquire()
        self.results.append(file_result)
        if not file_result.is_success:
            self.n_failed += 1
        self._set_worker_file(workerID)

        self.print_update(file_result)
        self.lock_worker.release()

    def start(self):
        """Start process."""
        self.print_start()
        self._init_workers()
        self.lock_worker.acquire()
        if self.v_level == VERBOSE_LEVEL_NORMAL:
            self.print_update(None)
        for idx, w in enumerate(self.workers):
            self.workers[idx].start()
            time.sleep(0.1)
        self.lock_worker.release()

        for idx, w in enumerate(self.workers):
            self.workers[idx].join()
        self.print_end()

    def _calc_percentage_processed(self, on=100):
        return int((len(self.results) * on) / self.n_file_to_send)

    def _create_failed_folder(self):
        folder_failed_resumes = os.path.join(os.getcwd(), FOLDER_NAME_FAILED_RESUMES)
        if not os.path.exists(folder_failed_resumes):
            try:
                os.makedirs(folder_failed_resumes)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    self.print_something('Warning: will not be able to copy failed files to the {} directory'.format(FOLDER_NAME_FAILED_RESUMES))
                    return False, ''
            except Exception as e:
                self.print_something('Warning: will not be able to copy failed files to the {} directory'.format(FOLDER_NAME_FAILED_RESUMES))
                return False, ''
        return True, folder_failed_resumes

    # _print_* functions don't actually print they just prepare a string that will be print after
    def _print_update_progress_bar(self):
        percent_proceed = self._calc_percentage_processed()
        progress_bar_processed = self._calc_percentage_processed(SIZE_PROGRESS_BAR)
        random_pic = random.randint(0, 5)

        bar = ''
        bar2 = ''
        for i in range(SIZE_PROGRESS_BAR):
            c = ' '
            if i < progress_bar_processed:
                c = '='
            bar += c
        bar = '[{}]'.format(bar)

        # Little points after the progress bar to be sure it hasn't crash :)
        for z in range(5):
            c = '.'
            if z == random_pic:
                c = ' '
            bar2 += c

        to_print = '{} %{} {}     \r'.format(bar, percent_proceed, bar2)
        return to_print

    def _print_finished_file(self, file_result, add_percentage=True):
        percent_proceed = self._calc_percentage_processed()
        file_data = {'file': file_result.file, 'sended': file_result.is_success, 'result': str(file_result.result)}
        file_data = json.dumps(file_data)
        if add_percentage:
            return '[%{}] - {}\n'.format(percent_proceed, file_data)
        return '{}\n'.format(file_data)

    def _print_all_file_to_send(self):
        to_send = ''
        for path in self.target:
            to_send += '{}\n'.format(path)
        return to_send

    def _print_numerical_datas(self, n_sended=False, n_total=False, n_failed=False):
        to_print = ''
        if n_sended:
            to_print += 'sended: {}\n'.format(self.n_file_to_send - self.n_failed)
        if n_failed:
            to_print += 'failed: {}\n'.format(self.n_failed)
        if n_total:
            to_print += 'total: {}\n'.format(self.n_file_to_send)
        return to_print

    # print_* function print on term
    def print_something(self, to_print, is_err=False, is_no_end=False):
        """Print on term."""
        # use of the printer lock to avoid message mixing
        # (not useful a the moment)
        self.lock_printer.acquire()
        out = sys.stdout
        end = '\n'
        if is_err:
            out = sys.stderr
        if is_no_end:
            end = ''
        print(to_print, file=out, end=end, flush=True)
        self.lock_printer.release()

    def print_start(self):
        """Print data a start."""
        if self.v_level == VERBOSE_LEVEL_SILENT:
            return
        to_print = ''
        if self.v_level != VERBOSE_LEVEL_SILENT:
            to_print = 'file to send: {}'.format(self._print_numerical_datas(n_total=True))
        if self.v_level == VERBOSE_LEVEL_VERBOSE:
            to_print += self._print_all_file_to_send()
        self.print_something(to_print)

    def print_update(self, last_file_result):
        """Print data when a file has been sent."""
        if self.v_level == VERBOSE_LEVEL_SILENT:
            return
        to_print = ''
        if self.v_level == VERBOSE_LEVEL_NORMAL:
            to_print = self._print_update_progress_bar()
            self.print_something(to_print, is_no_end=True)
        if self.v_level == VERBOSE_LEVEL_VERBOSE:
            to_print = self._print_finished_file(last_file_result)
            to_print = to_print[:-1]
            self.print_something(to_print)
        # Print to a file logs of all file result (like the verbose mode)
        # Uselful to keep track of all files and get the shinny progress bar at the same time
        if self.logfile is not None and last_file_result is not None:
            to_print = self._print_finished_file(last_file_result, add_percentage=False)
            self.logfile.write(to_print)

    def print_end(self):
        """Print data when all process is done."""
        if self.v_level == VERBOSE_LEVEL_SILENT:
            return
        to_print = ''
        to_print_file = ''
        # print all result
        if self.v_level == VERBOSE_LEVEL_VERBOSE:
            for res in self.results:
                to_print_file += self._print_finished_file(res, add_percentage=False)
            to_print += self._print_numerical_datas(n_total=True, n_sended=True, n_failed=True)
            self.print_something(to_print_file, is_err=True)
            self.print_something(to_print)
            return
        # print failed results
        if self.v_level == VERBOSE_LEVEL_NORMAL:
            for res in self.results:
                if not res.is_success:
                    to_print_file += self._print_finished_file(res, add_percentage=False)
            to_print += self._print_numerical_datas(n_total=True, n_sended=True, n_failed=True)
            self.print_something(to_print_file, is_err=True)
            self.print_something(to_print)
