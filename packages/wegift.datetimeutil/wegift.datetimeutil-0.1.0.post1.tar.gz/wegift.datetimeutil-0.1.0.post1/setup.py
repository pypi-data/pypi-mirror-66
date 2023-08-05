#!/usr/bin/env python3

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os

from setuptools import (find_packages,
                        setup)


def load_long_description() -> str:
    """Load the long description from the README file.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.rst')) as readme_file:
        return readme_file.read()


setup(
    name='wegift.datetimeutil',

    # Versions should comply with PEP 440.
    # See <https://www.python.org/dev/peps/pep-0440/>.
    version='0.1.0.post1',

    description='Util functions to work with timezone aware timestamps',
    # long_description=load_long_description(),  # TODO: provide long description

    # The project's main homepage
    url='https://gitlab.com/wegift/datetimeutil',

    # Author details
    author='WeGift',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Python versions supported
        'Programming Language :: Python :: 3.6',
    ],

    keywords='datetime date time timezone',

    namespace_packages=['wegift'],
    packages=find_packages(),

    install_requires=[
        'arrow',
        'pytz',
    ],
    extras_require={
        'test': ['mypy',
                 'pycodestyle',
                 'pylint',
                 'pytest'],
    }
)
