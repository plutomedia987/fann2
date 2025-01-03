#!/usr/bin/python

from setuptools import setup, Extension, find_packages
import glob
import os
import sys
import pathlib

NAME = 'fann2'
VERSION = '1.0.0'

LONG_DESCRIPTION = """\
    Fast Artificial Neural Network Library (FANN) implements multilayer
artificial neural networks with support for both fully connected
and sparsely connected networks. It includes a framework for easy
handling of training data sets. It is easy to use, versatile, well
documented, and fast.

FANN 2.2.0 source:
http://sourceforge.net/projects/fann/files/fann/2.2.0/FANN-2.2.0-Source.zip/download

"""


def find_executable(executable, path=None):
    """Try to find 'executable' in the directories listed in 'path' (a
    string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH']).  Returns the complete filename or None if not
    found
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    extlist = ['']
    if os.name == 'os2':
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == 'win32':
        pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
    for ext in extlist:
        execname = executable + ext
        if os.path.isfile(execname):
            return execname
        else:
            for p in paths:
                f = os.path.join(p, execname)
                if os.path.isfile(f):
                    return f
    else:
        return None


def find_swig():
    for executable in ("swig2.0", "swig"):
        if find_executable(executable):
            return executable
    raise Exception("Couldn't find swig2.0 binary!")


def build_swig(): 
    
    print("running swig")
    swig_bin = find_swig()
    swig_cmd = '%s -c++ -python fann2/fann2.i' % swig_bin
    print('Running SWIG before:', swig_cmd)
    os.system(swig_cmd)

if "sdist" not in sys.argv:
    # These lines are needed to circumvent a bug in distutils
    build_swig()

# This utility function searches for files
def hunt_files(root, which):
    return glob.glob(os.path.join(root, which))

def fann_lib():
    #Add libraries to sys path
    installLoc = str(list(pathlib.Path("/").glob("**/config/custom_libraries/libfann"))[0])
    if installLoc not in sys.path:
        sys.path.append(installLoc)   
        
    return installLoc

setup(
    name=NAME,
    description='Fast Artificial Neural Network Library (fann)',
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author='Steffen Nissen',
    author_email='lukesky@diku.dk',
    maintainer='Gil Megidish, Vincenzo Di Massa and FutureLinkCorporation',
    maintainer_email='gil@megidish.net & hawk.it@tiscali,it and devel@futurelinkcorporation.com',
    url='https://github.com/FutureLinkCorporation/fann2',
    license='GNU LESSER GENERAL PUBLIC LICENSE (LGPL)',
    dependency_links=[
        "http://www.swig.org/download.html#egg"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Programming Language :: Python :: 2.7"
    ],
    keywords="ANN artificial intelligence FANN2.2.0 bindings".split(' '),
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    py_modules=['fann2.libfann'],
    install_requires=[ 
        "swig", 
    ],
    ext_modules=[Extension('fann2._libfann', ['fann2/fann2_wrap.cxx'],
                           include_dirs=['./include',
                                         '../include', 'include'],
                           libraries=['doublefann'],
                           library_dirs=[fann_lib()],
                           runtime_library_dirs=[fann_lib()],
                           define_macros=[("SWIG_COMPILE", None)]
                           ),
                 ]
)

# "http://sourceforge.net/projects/fann/files/fann/2.2.0/FANN-2.2.0-Source.zip/download",
