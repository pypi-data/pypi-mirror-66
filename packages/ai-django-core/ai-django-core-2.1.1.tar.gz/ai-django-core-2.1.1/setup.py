#!/usr/bin/env python
import ast
import re

from setuptools import find_packages, setup

# Dependencies
requirements = [
    'django-crispy-forms>=1.4.0',
    'Django>=1.7.0',
    'bleach>=1.4.2',
    'python-dateutil>=2.5.3',
    'future>=0.16',
    'freezegun',
    'pytest-cov',
    'pytest-django',
    'pytest-mock',
]

# Parse version
_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("ai/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

setup(
    name='ai-django-core',
    version=version,
    author='Ambient Innovation: GmbH',
    author_email='hello@ambient-innovation.com',
    packages=find_packages(),
    include_package_data=True,
    license="The MIT License (MIT)",
    description='Lots of helper functions and useful widgets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    install_requires=requirements
)
