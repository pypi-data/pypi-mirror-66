from __future__ import print_function, division, absolute_import
# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2020 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tarfile
from contextlib import contextmanager

import requests

FILE_NAME = "gsl-latest.tar.gz"
URL = "http://mirror.inode.at/gnu/gsl/" + FILE_NAME


@contextmanager
def run_in_folder(folder):
    current_folder = os.getcwd()
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        os.chdir(folder)
        yield
    finally:
        os.chdir(current_folder)


def download_if_needed(download_folder):

    with run_in_folder(download_folder):
        if not os.path.exists(FILE_NAME):
            print("download source code from", URL)
            with open(FILE_NAME, "wb") as fh:
                fh.write(requests.get(URL).content)


def decompress_if_needed(download_folder):
    with run_in_folder(download_folder):
        with tarfile.open(FILE_NAME, "r") as fh:
            gsl_folder = fh.getnames()[0]
            if not os.path.exists(gsl_folder):
                print("extract", FILE_NAME)
                fh.extractall()
        return os.path.join(download_folder, gsl_folder)


def configure_if_needed(folder, target):
    with run_in_folder(folder):
        if not os.path.exists("Makefile"):
            assert (
                os.system("./configure --prefix={target}".format(target=target)) == 0
            ), "running configure failed"


def run_make_if_needed(folder):
    with run_in_folder(folder):
        if not os.path.exists("./statistics/ttest.o"):
            assert os.system("make") == 0, "running make failed"


def run_make_install_if_needed(gsl_folder, target_folder):
    with run_in_folder(gsl_folder):
        if not all(
            os.path.exists(os.path.join(target_folder, sub_folder))
            for sub_folder in ("lib", "bin", "include")
        ):
            assert os.system("make install") == 0, "running make install failed"


def install_gsl_if_needed(download_folder, target_folder):
    download_if_needed(download_folder)
    gsl_folder = decompress_if_needed(download_folder)
    configure_if_needed(gsl_folder, target_folder)
    run_make_if_needed(gsl_folder)
    run_make_install_if_needed(gsl_folder, target_folder)


if __name__ == "__main__":
    install_gsl_if_needed("/tmp/gsl_download", "/tmp/gsl_installation")
