import setuptools
from tensorcircuit import __version__, __author__


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tensorcircuit",
    version=__version__,
    author=__author__,
    author_email="refraction-ray@protonmail.com",
    description="Quantum circuits on top of tensor network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/refraction-ray/tensorcircuit",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "scipy", "tensornetwork"],
    tests_require=["pytest"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
