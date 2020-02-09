from setuptools import setup, find_packages
import pathlib
import versioneer

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="svl",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/timothyrenner/svl",
    packages=find_packages(
        exclude=[
            "sample_data",
            "sample_scripts",
            "sample_visualizations",
            "build",
            "dist",
            "graffle",
            "site",
            "test",
            "docs",
        ]
    ),
    include_package_data=True,
    license="MIT",
    author="Tim Renner",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "click>=6.7,<7.0",
        "toolz>=0.9.0,<1.0",
        # Lark's made some backward incompatible changes, so pin this one
        # and upgrade with caution.
        "lark-parser==0.6.6",
        "Jinja2>=2.10.1",
        "pandas>=0.25.0,<1.0.0",
        "importlib-resources>=1.0.2,<2",
    ],
    extras_require={"parquet": ["pyarrow>=0.12.0"]},
    entry_points={"console_scripts": ["svl=svl.cli:cli"]},
)
