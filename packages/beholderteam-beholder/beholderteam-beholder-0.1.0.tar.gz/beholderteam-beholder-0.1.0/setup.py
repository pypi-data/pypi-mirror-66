import setuptools
from pathlib import Path

from setuptools import find_namespace_packages

long_description = Path("README.md").read_text()

setuptools.setup(
    name="beholderteam-beholder",
    version="0.1.0",
    author="beholder-devteam",
    maintainer="beholder_devteam",
    description="A simple tool to monitor selected websites",
    long_description=long_description,
    packages=find_namespace_packages(include=('beholder', 'beholder.*')),
    install_requires=(
        'requests==2.23.0',
    ),
    extras_require={
        'dev': (
            'pytest==5.4.1',
            'pytest-mock==2.0.0',
            'pytest-cov==2.8.1',
            'mypy==0.770',
            'flake8==3.7.9',
            'flake8-commas==2.0.0',
        ),
    },
    python_requires='>=3.8.0',
)
