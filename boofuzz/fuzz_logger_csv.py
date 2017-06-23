from __future__ import print_function
from builtins import bytes
import sys
import time
import datetime
import csv

from . import helpers
from . import ifuzz_logger_backend

from IPython import embed

init()

def hex_to_hexstr(input_bytes):
    """
    Render input_bytes as ASCII-encoded hex bytes, followed by a best effort
    utf-8 rendering.

    @param input_bytes: Arbitrary bytes.

    @return: Printable string.
    """
    #return helpers.hex_str(input_bytes) + " " + repr(bytes(input_bytes))
    return '0x' + ''.join("{:02x}".format(ord(b)) for b in input_bytes)

DEFAULT_HEX_TO_STR = hex_to_hexstr


def get_time_stamp():
    # t = time.time()
    # s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    # s += ",%03d]" % (t * 1000 % 1000)
    # s = t.isoFormat()
    s = datetime.datetime.utcnow().isoformat()
    return s


class FuzzLoggerCsv(ifuzz_logger_backend.IFuzzLoggerBackend):
    """
    This class formats FuzzLogger data for pcap file. It can be
    configured to output to a named file.
    """

    def __init__(self, file_handle=sys.stdout, bytes_to_str=DEFAULT_HEX_TO_STR):
        """
        @type file_handle: io.FileIO
        @param file_handle: Open file handle for logging. Defaults to sys.stdout.

        @type bytes_to_str: function
        @param bytes_to_str: Function that converts sent/received bytes data to string for logging.
        """
        self._file_handle = file_handle
        self._format_raw_bytes = bytes_to_str
        self._csv_handle = csv.writer(self._file_handle)

    def open_test_step(self, description):
        None

    def log_check(self, description):
        None

    def log_error(self, description):
        None

    def log_recv(self, data):
        self._print_log_msg(["recv", self._format_raw_bytes(data),data])

    def log_send(self, data):
        self._print_log_msg(["send", self._format_raw_bytes(data),data])

    def log_info(self, description):
        None

    def open_test_case(self, test_case_id):
        self._print_log_msg(["", "", ""])

    def log_fail(self, description=""):
        None

    def log_pass(self, description=""):
        None

    def _print_log_msg(self, msg, indent_level=0):
        time_stamp = get_time_stamp()
        self._csv_handle.writerow([time_stamp] + msg)