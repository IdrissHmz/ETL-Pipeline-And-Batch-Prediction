import argparse
import ftplib
import multiprocessing as mp
import os
import re
import signal
import tempfile
from xmlrpc.client import FastParser
import tensorflow as tf
import zlib
from io import BytesIO

_USER_RE = r"""(?P<user>[^:@]+|'[^']+'|"[^"]+")"""
_PASSWORD_RE = r"""(?P<password>[^@]+|'[^']+'|"[^"]+")"""
_CREDS_RE = r"{}(?::{})?".format(_USER_RE, _PASSWORD_RE)
FTP_RE = re.compile(r"^ftp://(?:{}@)?(?P<abs_path>.*)$".format(_CREDS_RE))

FORCE_DISABLE_MULTIPROCESSING = False

data_dir = "results/data"

filter_regex = r"\.sdf"

data_source = [
    "ftp://anonymous:guest@ftp.ncbi.nlm.nih.gov/"
    "pubchem/Compound_3D/01_conf_per_cmpd/SDF"
]


filter_re = re.compile(filter_regex)
ftp_files = []

m = FTP_RE.search(data_source[0])
print(m)
if not m:
    raise ValueError("malformed FTP URI")
user = m.group("user") or "anonymous"
password = m.group("password") or "guest"
server, path_dir = m.group("abs_path").split("/", 1)
uri_prefix = "ftp://{}:{}@{}/".format(user, password, server)

ftp = ftplib.FTP(server, user, password)
ftp_files += [
    {"user": user, "password": password, "server": server, "path": path,}
    for path in ftp.nlst(path_dir)
    if filter_re.search(uri_prefix + path)
]
ftp.quit()
print(user, "\n", password, "\n", server, "\n", path_dir, "\n", uri_prefix, "\n")

ftp_file_to_download = ftp_files[0]


basename = os.path.basename(ftp_file_to_download.path)
sdf_file = os.path.join(data_dir, os.path.splitext(basename)[0])

if not tf.io.gfile.exists(sdf_file):

    memfile = BytesIO()
    ftp = ftplib.FTP(server, user, password)
    ftp.retrbinary("RETR " + ftp_file_to_download.path, memfile.write)
    ftp.quit()

    memfile.seek(0)
    with tf.io.gfile.GFile(sdf_file, "w") as f:
        gzip_wbits_format = zlib.MAX_WBITS | 16
        contents = zlib.decompress(memfile.getvalue(), gzip_wbits_format)
        f.write(contents)
    print("Extracted {}".format(sdf_file))

else:
    print("Found {}".format(sdf_file))
