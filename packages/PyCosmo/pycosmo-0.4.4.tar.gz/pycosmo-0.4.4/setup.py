# Copyright (C) 2013 - 2020 ETH Zurich, SIS ID with Institute of Astronomy and Particle
# Physics.
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
import sys

from setuptools import Distribution, Extension, find_packages, setup

required = [
    "numpy",
    "sympy<1.4",
    "scipy>=0.14.0",
    "recfast4py>=0.1.1",
    "Cython",
    "dill",
    "numba",
]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        # file might not exist when package is installed as dependency:
        return ""


class BinaryDistribution(Distribution):

    """as this setup.py does not declare c code to compile, 'setup.py bdist_wheel'
    would create source wheels, unless we implement this 'fake' class and use
    it as 'distclass=BinaryDistribution' below.
    """

    def has_ext_modules(self):
        return True


def create_ext_modules():
    """
    Build commands require preinstalled numpy to compile the c extensions. A
    global "import numpy" here would break tox and also if installed as a
    dependency from another python package. So we only require numpy for the
    cases where its header files are actually needed.
    """

    build_commands = (
        "build",
        "build_ext",
        "build_py",
        "build_clib",
        "build_scripts",
        "bdist_wheel",
        "bdist_rpm",
        "bdist_wininst",
        "bdist_msi",
        "bdist_mpkg",
        "build_sphinx",
        "develop",
        "install",
        "install_lib",
        "install_header",
    )

    ext_modules = []
    if any(command in build_commands for command in sys.argv[1:]):
        try:
            import numpy
        except ImportError:
            raise Exception(
                "please install numpy, need numpy header files to compile c extensions"
            )

        from Cython.Build import cythonize

        cythonize("PyCosmo/cython/halo_integral.pyx")
        files = [
            "const.c",
            "main.c",
            "halo_integral.c",
            "polevl.c",
            "sici.c",
            "sicif.c",
            "polevlf.c",
            "logf.c",
            "sinf.c",
            "constf.c",
            "mtherr.c",
        ]
        ext_modules = [
            Extension(
                "PyCosmo.cython.halo_integral",
                sources=["PyCosmo/cython/" + file for file in files],
                include_dirs=[numpy.get_include()],
            )
        ]
    return ext_modules



setup(
    name="pycosmo",
    version="0.4.4",  # no need to update version in other places of PyCosmo
    author="Alexandre Refregier",
    author_email="alexandre.refregier@phys.ethz.ch",
    url="http://cosmo-docs.phys.ethz.ch/PyCosmo",
    license="Proprietary",
    packages=find_packages(exclude=["examples", "tests.param_files", "tests"]),
    description="A multi-purpose cosmology calculation tool",
    long_description=read("README.rst"),
    install_requires=required,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: C",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    distclass=BinaryDistribution,
    ext_modules=create_ext_modules(),
)
