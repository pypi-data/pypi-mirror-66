#!/usr/bin/python3
"""Uploads resume on hrflow platform."""
import argparse
import sys

from .supervisor import Supervisor, VALID_EXTENSIONS, INVALID_FILENAME

import hrflow as hf


def parse_args():
    """Parse command line argument."""
    argsParser = argparse.ArgumentParser(description='Send resume to the platform.')
    argsParser.add_argument('--target', nargs='*', required=True)
    argsParser.add_argument('--is_recurcive', action='store_const', const=True, default=False)
    argsParser.add_argument('--source_id', default=None)
    argsParser.add_argument('--sleep', default=0)
    argsParser.add_argument('--api_key', default=None)
    argsParser.add_argument('--api_url', default="https://api.hrflow.ai/v1/")
    argsParser.add_argument('--timestamp_reception', default=None)
    argsParser.add_argument('--verbose', action='store_const', const=True, default=False)
    argsParser.add_argument('--silent', action='store_const', const=True, default=False)
    argsParser.add_argument('--n-worker', default=3)
    argsParser.add_argument('--logfile', default=None, required=False)
    args = argsParser.parse_args()
    return args


def get_from_stdin(message):
    """Prompt a message and wait for user input."""
    print(message, end='', flush=True)
    res = sys.stdin.readline()
    res = res[:-1]
    return res


def get_user_data(args):
    """Get command line missing datas."""
    if args.api_key is None:
        args.api_key = get_from_stdin('api secret key: ')
    if args.source_id is None:
        args.source_id = get_from_stdin('source id: ')
    return args


def main():
    """Well..."""
    # Prepare upload
    args = parse_args()
    args = get_user_data(args)
    # Start upload.
    client = hf.Client(api_secret=args.api_key, api_url=args.api_url)
    supervisor = Supervisor(client, args.source_id, args.target, args.timestamp_reception, args.is_recurcive,
                            args.silent, args.verbose, args.sleep, args.n_worker, args.logfile)
    supervisor.start()


if __name__ == '__main__':
    main()
