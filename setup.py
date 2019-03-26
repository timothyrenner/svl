
from setuptools import setup, find_packages
import versioneer

setup(
    name='svl',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["scripts/", "data/"]),
    license='MIT',
    author="Tim Renner",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python :: 3.5",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7"
    ],
    install_requires=[
        'click==6.7',
        'toolz==0.9.0',
        'lark-parser==0.6.6',
        'Jinja2==2.10',
        'pandas==0.23.4'
    ],
    extras_require={
        "parquet": ["pyarrow==0.12.0"]
    },
    entry_points={
        "console_scripts": ["svl=svl.cli:cli"]
    }
)
