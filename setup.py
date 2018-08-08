
from setuptools import setup, find_packages

setup(
    name='svl',
    version='0.1.dev',
    packages=find_packages(exclude=["scripts/", "data/"]),
    license='MIT',
    author="Tim Renner",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Programming Language :: Python :: 3.6"
    ],
    install_requires=[
        'click',
        'toolz',
        'lark-parser',
        'jinja2'
    ],
    entry_points={
        "console_scripts": ["svl=svl.cli:cli"]
        }
)
