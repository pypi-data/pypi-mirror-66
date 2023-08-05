#!/usr/bin/env python
import setuptools
import sys

if sys.platform in ['darwin', 'linux', 'linux2']:
    extras_require = {}
elif sys.platform in ['win32']:
    extras_require = {
        'win32': 'pypiwin32'
    }

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mocherry",
    version="1.0.5",
    author="Sougata P.",
    author_email="skall.paul@gmail.com",
    description="CherryPy REST webservice framework with MongoDB ORM support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techunits/mocherry",
    download_url="https://github.com/techunits/mocherry/archive/1.0.5.tar.gz",
    packages=setuptools.find_packages(),
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    setup_requires=[
        'cherrypy',
        'wheel'
    ],
    install_requires=[
        'mongoengine',
        'routes',
        'cherrypy_cors',
        'requests'
    ],
    entry_points = {
        'console_scripts': [
            'mocherry-cli=mocherry.library.cli.commands:execute_command'
        ]
    },
    extras_require=extras_require,
    python_requires='>=3.6',
)
