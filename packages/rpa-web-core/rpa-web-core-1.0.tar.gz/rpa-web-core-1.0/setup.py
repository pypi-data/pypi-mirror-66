# -*- coding: utf-8 -*-

"""
RPA Web Core | rpa-web-core
Core packages for web based Robot Process Automation Tasks
"""

from os.path import abspath, dirname, join
from setuptools import setup


LIBRARY_NAME = "rpa-web-core"
CWD = abspath(dirname(__file__))


description = "Core packages for web based Robot Process Automation Tasks"
dependencies = [
    'robotframework',
    'robotframework-seleniumlibrary',
]
# Get the long description from the README file
with open(join(CWD, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

CLASSIFIERS = """
Development Status :: 3 - Alpha
Topic :: Software Development :: Testing
Operating System :: OS Independent
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
""".strip().splitlines()

setup(
    version="1.0",
    name=LIBRARY_NAME,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avimehenwal/rpa-web-core",
    author="Avi Mehenwal",
    author_email="avi.mehanwal@gmail.com",
    license="GNU License 2.0",
    classifiers=CLASSIFIERS,
    keywords="robot framework testing automation selenium seleniumlibrary robot process rpa",
    platforms="any",
    packages=[LIBRARY_NAME],
    package_dir={"": "src"},
    package_data={LIBRARY_NAME: ["rf-resources/*.resource"]},
    # install_requires=dependencies,
)