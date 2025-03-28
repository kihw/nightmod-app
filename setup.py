#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de configuration pour NightMod
Permet l'installation via pip (pip install .)
"""

from setuptools import setup, find_packages
import os
import re

# Lire la version depuis src/__init__.py
def get_version():
    init_py = open(os.path.join('src', '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

# Lire le contenu du README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Lire les dépendances depuis requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="nightmod",
    version=get_version(),
    author="NightMod Team",
    author_email="contact@nightmod.example.com",
    description="Surveillant de sommeil et économiseur d'énergie",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kihw/nightmod",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Gnome",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Topic :: Utilities",
    ],
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "nightmod=nightmod:main",
        ],
        "gui_scripts": [
            "nightmod-gui=nightmod:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nightmod": [
            "assets/*.ico",
            "assets/*.png",
            "assets/*.wav",
            "themes/*.tcl",
        ],
    },
    # Dépendances optionnelles
    extras_require={
        "tray": ["pystray", "pillow"],
        "system": ["psutil"],
        "all": ["pystray", "pillow", "psutil"],
    },
)