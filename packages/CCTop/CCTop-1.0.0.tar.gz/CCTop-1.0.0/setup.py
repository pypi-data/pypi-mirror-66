#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CCTop",
    version="1.0.0",
    packages=["cctop"],
    
    python_requires=">=3.5",
    
    extras_require={
        "bx":  ["bx-python"],
    },
    
    entry_points = {
        'console_scripts': ['cctop=cctop.CCTop:main',
        'gff2bedFiles=cctop.gff2bedFiles:main'],
    },
    
    author="Juan L. Mateo",
    author_email="mateojuan@uniovi.es",
    description="CRISPR/Cas Target online predictor",
    long_description = long_description,
    long_description_content_type="text/markdown",
    keywords="CRISPR",
    url="https://bitbucket.org/juanlmateo/cctop_standalone",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License"
    ],
)
