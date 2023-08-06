#!/usr/bin/env python
from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="pwbus",
    version="0.0.28",
    author="Fabio Szostak",
    author_email="fszostak@gmail.com",
    description="A simple task execution manager with integration bus cababities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fszostak/pwbus",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    entry_points={
        'console_scripts': ['pwbus=pwbus.cli.command_line:main'],
    },
    install_requires=requirements,
    setup_requires=['flake8'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)
