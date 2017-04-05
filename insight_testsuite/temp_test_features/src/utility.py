#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This module contains:
    A modified logger class inherited from logging.Logger.
    A function memory_usage() that returns the memory used.
"""
import logging
import os
import sys

class Logger(logging.Logger):
    """
    A modified logger class inherited from logging.Logger.
    """
    def __init__(self, workspace):
        """
        Initialize the logger.
        Assign a stream_handler and a file_handler to the logger.
        The log file is writen in the specified workspace.
        Args:
            workspace: the directory to put the log file.
        """
        super(Logger, self).__init__(__name__)
        #self.log = logging.getLogger()
        self.setLevel(logging.INFO)

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler(os.path.join(workspace, 'process.log'))

        self.stream_handler.setLevel(logging.INFO)
        self.file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s]:\n%(message)s",
                                      datefmt='%y/%m/%d %H:%M:%S')

        self.stream_handler.setFormatter(formatter)
        self.file_handler.setFormatter(formatter)

        self.addHandler(self.stream_handler)
        self.addHandler(self.file_handler)

    # pylint: disable=invalid-name
    def Abort(self, msg):
        """
        Print out the error msg to the stream and log file and raise an AssertionError.
        Args:
            msg(str): the error message to print out.
        Raises:
            AssertionError
        """
        self.error(msg)
        raise AssertionError

def memory_usage():
    """
    Return the memory used in the job.
    Returns:
        mem(float): the memory used in units of MB.
    """
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
                           stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem
