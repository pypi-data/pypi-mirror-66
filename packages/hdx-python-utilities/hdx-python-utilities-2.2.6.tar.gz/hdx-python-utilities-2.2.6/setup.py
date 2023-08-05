# -*- coding: utf-8 -*-
import sys
from os.path import join

from setuptools import setup, find_packages

sys.path.append('src')  # Only needed for this project
from hdx.utilities import CleanCommand, PackageCommand, PublishCommand
from hdx.utilities.loader import load_file_to_str

requirements = ['basicauth',
                'beautifulsoup4',
                'colorlog',
                'email_validator',
                'html5lib',
                'psycopg2-binary',
                'pyaml',
                'python-dateutil==2.8.1',
                'ratelimit',
                'six>=1.14.0',
                'sshtunnel',
                'tabulator[cchardet]>=1.38.2',
                'typing',
                'yamlloader'
                ]

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

PublishCommand.version = load_file_to_str(join('src', 'hdx', 'utilities', 'version.txt'), strip=True)

setup(
    name='hdx-python-utilities',
    description='HDX Python Utilities',
    license='MIT',
    url='https://github.com/OCHA-DAP/hdx-python-utilities',
    version=PublishCommand.version,
    author='Michael Rans',
    author_email='rans@email.com',
    keywords=['HDX', 'utilities', 'library', 'country', 'iso 3166'],
    long_description=load_file_to_str('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=True,
    classifiers=classifiers,
    install_requires=requirements,
    cmdclass={'clean': CleanCommand, 'package': PackageCommand, 'publish': PublishCommand},
)
