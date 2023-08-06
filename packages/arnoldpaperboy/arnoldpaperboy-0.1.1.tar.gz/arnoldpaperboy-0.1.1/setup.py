# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.
# pylint: skip-file
from setuptools import setup, find_packages

version = '0.1.1'

long_description = open('README.rst').read()

requirements = [
    'dealer',
    'google-cloud-logging',
    'google-cloud-monitoring',
]

test_requirements = [
    'pytest',
]

setup(
    name='arnoldpaperboy',
    version=version,
    description="Deliver to stackdriver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Satelligence",
    author_email='schut@satelligence.com',
    url='https://gitlab.com/satelligence/arnoldpaperboy',
    packages=find_packages(),
    include_package_data=True,
    license="Apache-2.0",
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=requirements,
)
