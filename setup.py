# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup module."""

from setuptools import setup

setup(
    name='selenol-platform',
    version='0.1.0',
    description='Base system to orchestrate selenol services.',
    url='https://github.com/selenol/selenol-platform',
    author='Javier Delgado',
    author_email='JavierDelgado@outlook.com',
    license='GPLv3',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'selenol=selenol_platform.cli:cli_group',
        ],
    },
    install_requires=[
        'Click>=6.7',
        'selenol-python>=0.1',
        'sqlalchemy>=1.1.9',
    ],
    packages=['selenol_platform'],
    extras_require={
        'tests': [
            'coverage>=4.0',
            'isort>=4.2.5',
            'pytest>=3.0.7',
            'pydocstyle>=1.1.1',
            'pytest-cache>=1.0',
            'pytest-cov>=2.4.0',
            'pytest-pep8>=1.0.6',
            'pytest-runner>=2.11.1',
        ],
    },
)
