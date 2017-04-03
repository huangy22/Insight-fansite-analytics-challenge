#!/usr/bin/env python
import logging
#import signal
import os,sys

#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir) 

workspace = "./"

log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler(os.path.join(workspace,'process.log'))

ch.setLevel(logging.INFO)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s]:\n%(message)s",
        datefmt='%y/%m/%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
log.addHandler(ch)
log.addHandler(fh)

def Assert(condition, info):
    if not condition:
        log.error(info)
        raise AssertionError

def Abort(info):
    log.error(info)
    raise AssertionError

def memory_usage():
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
    stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem
