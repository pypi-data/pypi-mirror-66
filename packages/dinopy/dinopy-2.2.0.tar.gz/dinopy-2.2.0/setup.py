# -*- coding: utf-8 -*-
import sys
from functools import partial

import numpy as np
from setuptools import setup, Extension
from Cython.Build import cythonize

Extension = partial(Extension, extra_compile_args=["-O3"], include_dirs=[np.get_include()])

# Collect all extension modules by cythonizing and compiling the .pyx files.
c_extensions = [
    Extension(
        "dinopy.{}".format(filename),
        ["dinopy/{}{}".format(filename, ".pyx")])
    for filename in
    ["auxiliary", "conversion", "creader", "definitions", "fasta_reader", "fasta_writer", "fastq_reader",
     "fastq_writer", "input_opener", "processors", "shape", "shaping", "output_opener", "nameline_parser", "sam_reader",
     "sam_writer", "sambam"]
]
cpp_extensions = [
    Extension(
        "dinopy.wrap_sais",
        ["dinopy/wrap_sais{}".format(".pyx")],
        include_dirs=['dinopy/cpp/'],
        language="c++",
    )]
extensions = c_extensions + cpp_extensions

extensions = cythonize(extensions, compiler_directives={
    'language_level': 3,
    'boundscheck': False,
    'nonecheck': False,
    'embedsignature': True,
})


setup(
    name='dinopy',
    description="DNA input and output library for Python and Cython. Includes reader and writer for FASTA and FASTQ "
                "files, support for samtools faidx files, and generators for solid and gapped q-grams (k-mers).",
    long_description=open("README.rst").read(),
    version='2.2.0',
    author='Henning Timm, Till Hartmann',
    author_email='henning.timm@tu-dortmund.de, till.hartmann@tu-dortmund.de',
    license="MIT",
    url="https://bitbucket.org/HenningTimm/dinopy",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Cython',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
    packages=['dinopy'],
    # Add cython and c++ files
    package_data={'dinopy': ['*.pyx', '*.pxd', 'cpp/sais.cpp', '../README.rst']},
    install_requires=['numpy>=1.17', 'cython>=0.22'],
    ext_modules=extensions,
)
