#! /usr/bin/env python
#
# Copyright (C) 2021 Kacper Sokol <ks1591@my.bristol.ac.uk>
# License: new BSD

from setuptools import find_packages, setup

import sphinx_term

DISTNAME = 'sphinx-term'
MAINTAINER = 'Kacper Sokol'
MAINTAINER_EMAIL = 'ks1591@my.bristol.ac.uk'
DESCRIPTION = ('A collection of Sphinx (and Jupyter Book) extensions '
               'for authoring vivacious terminal transcripts.')
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
LONG_DESCRIPTION_CT = 'text/markdown'
LICENCE = 'new BSD'
VERSION = sphinx_term.__version__
URL = 'https://github.com/So-Cool/{}'.format(DISTNAME)
DOWNLOAD_URL = 'https://pypi.org/project/{}/#files'.format(DISTNAME)
PYTHON_REQUIRES = '~=3.5'  # Python 3.5 and up but not yet Python 4
INSTALL_REQUIRES = ['docutils', 'sphinx>=3', 'pyyaml']
PACKAGES = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests'])
INCLUDE_PACKAGE_DATA = True
ZIP_SAFE = False  # We are using static files

def setup_package():
    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    long_description=LONG_DESCRIPTION,
                    long_description_content_type=LONG_DESCRIPTION_CT,
                    license=LICENCE,
                    version=VERSION,
                    url=URL,
                    download_url=DOWNLOAD_URL,
                    python_requires=PYTHON_REQUIRES,
                    install_requires=INSTALL_REQUIRES,
                    packages=PACKAGES,
                    include_package_data=INCLUDE_PACKAGE_DATA,
                    zip_safe=ZIP_SAFE)
    setup(**metadata)

if __name__ == '__main__':
    setup_package()
