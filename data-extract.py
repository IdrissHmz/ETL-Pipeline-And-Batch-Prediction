import argparse
import ftplib
import multiprocessing as mp
import os
import re
import signal
import tempfile
import tensorflow as tf
import zlib
from io import BytesIO

_USER_RE = r"""(?P<user>[^:@]+|'[^']+'|"[^"]+")"""
_PASSWORD_RE = r"""(?P<password>[^@]+|'[^']+'|"[^"]+")"""
_CREDS_RE = r"{}(?::{})?".format(_USER_RE, _PASSWORD_RE)
FTP_RE = re.compile(r"^ftp://(?:{}@)?(?P<abs_path>.*)$".format(_CREDS_RE))

FORCE_DISABLE_MULTIPROCESSING = False
