import sys

PYTHONMAJORVERSION = sys.version_info[0]


def strToBytes(s):
    if PYTHONMAJORVERSION <= 2:
        return bytearray(s)
    else:
        return s.encode('utf-8')
