# auto generated by update_py.py
from datetime import datetime
import sys
import os

def nano_to_str(nano, fmt='%Y%m%d-%H:%M:%S'):
    ts = nano / 1e9
    return datetime.utcfromtimestamp(ts).strftime(fmt)

def bytify(ss):
    if sys.version_info < (3, 0):
        data = bytes(ss)
    else:
        data = bytes(ss, 'utf8')
    return data

def get_windows_first_disk():
    for i in range(65, 91):
        vol = chr(i) + ":"
        if os.path.isdir(vol):
            return vol

    raise EnvironmentError("could not get the right disk")

def get_log_default_path():
    # python2: linux2, python3: linux
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        dirs = "/shared/log"
    elif sys.platform == "win32":
        dirs = os.path.join(get_windows_first_disk() + "/tmp/linker/log")
    else:
        dirs = '.'

    return dirs

def get_today_date():	
    return datetime.today().strftime('%Y-%m-%d')
