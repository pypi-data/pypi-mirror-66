# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

setup(
    # package name
    name='hrflow-importer',
    # code version
    version="1.0.0",
    # so far ignore paragraph embedding part for package
    packages=find_packages(),
    author="hrflow",
    author_email="dev@hrflow.ai",
    description="Hrflow importer",
    install_requires=["hrflow"],
    include_package_data=True,
    package_data={'manager': ['drawers/prod_ner_drawer_icons/*.png']},
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': [
            'resumeImporter = importer:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
    ]
)