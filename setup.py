
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
        'click==6.7',
        'toolz==0.9.0',
        'lark-parser==0.5.6',
        'Jinja2==2.10',
        'maya==0.5.0'
    ],
    entry_points={
        "console_scripts": ["svl=svl.cli:cli"]
    },
    extras_require={
        "pandas": ["pandas==0.23.4"]
    }
)
