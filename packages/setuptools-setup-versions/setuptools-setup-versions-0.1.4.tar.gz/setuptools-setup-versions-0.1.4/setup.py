from setuptools import setup, find_packages

setup(
    name='setuptools-setup-versions',
    version="0.1.4",
    description=(
        "Automatically update setup.py `install_requires` version numbers"
        "for PIP packages"
    ),
    author='David Belais',
    author_email='david@belais.me',
    python_requires='~=3.6',
    keywords='setuptools install_requires version',
    packages=find_packages(),
    install_requires=[
        "setuptools~=46.1",
        "pip~=20.0",
        "more-itertools~=8.2"
    ],
    extras_require={
        "test": [
            "tox~=3.14",
            "pytest~=5.4"
        ],
        "dev": [
            "tox~=3.14",
            "pytest~=5.4",
            "wheel~=0.34",
            "readme-md-docstrings>=0.0.10,<1"
        ]
    }
)
