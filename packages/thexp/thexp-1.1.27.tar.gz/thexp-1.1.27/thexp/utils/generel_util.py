"""
    Copyright (C) 2020 Shandong University

    This program is licensed under the GNU General Public License 3.0 
    (https://www.gnu.org/licenses/gpl-3.0.html). 
    Any derivative work obtained under this license must be licensed 
    under the GNU General Public License as published by the Free 
    Software Foundation, either Version 3 of the License, or (at your option) 
    any later version, if this derivative work is distributed to a third party.

    The copyright for the program is owned by Shandong University. 
    For commercial projects that require the ability to distribute 
    the code of this program as part of a program that cannot be 
    distributed under the GNU General Public License, please contact 
            
            sailist@outlook.com
             
    to purchase a commercial license.
"""
import hashlib
import os
import sys
from datetime import datetime


def listdir_by_time(dir_path):
    dir_list = os.listdir(dir_path)
    if not dir_list:
        return []
    else:
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getatime(os.path.join(dir_path, x)), reverse=True)
        return dir_list


def home_dir():
    path = os.path.expanduser("~/.thexp")
    os.makedirs(path, exist_ok=True)
    return path


def file_atime_hash(file):
    return string_hash(str(os.path.getatime(file)))


def string_hash(*str):
    hl = hashlib.md5()
    for s in str:
        hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()[:16]


def file_hash(file):
    hl = hashlib.md5()
    with open(file, encoding="utf-8") as r:
        s = "".join(r.readlines())
        hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()[:16]


def curent_date(fmt='%y-%m-%d-%H%M%S', dateobj: datetime = None):
    if dateobj is not None:
        return dateobj.strftime(fmt)
    return datetime.now().strftime(fmt)


def file_atime2date(file, fmt='%y%m%d-%H%M%S'):
    return curent_date(fmt, datetime.fromtimestamp(os.path.getatime(file)))


def path_equal(p1, p2):
    return os.path.normcase(p1) == os.path.normcase(p2)


def path_in(sub, all):
    return os.path.normcase(sub) in os.path.normcase(all)


class exithook():
    def __init__(self):
        self.exit_code = None
        self.exception = None

    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc, *args):
        self.exception = exc

def iter2pair(obj):
    for k in obj:
        if isinstance(obj,dict):
            yield k, obj[k]
        elif isinstance(k, (list, tuple)):
            yield k[0], k[1]
        elif isinstance(k, dict):
            for kk, vv in k.items():
                yield kk, vv

