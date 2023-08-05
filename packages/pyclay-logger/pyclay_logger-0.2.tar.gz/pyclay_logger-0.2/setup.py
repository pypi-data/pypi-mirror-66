from setuptools import setup, find_packages
import logger as pkg

packages = find_packages(
        where='.',
        include=['logger*']
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyclay_logger',
    version=pkg.__version__,
    description='logger library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cm107/logger",
    author='Clayton Mork',
    author_email='mork.clayton3@gmail.com',
    license='MIT License',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pylint>=2.4.2',
        'twine>=3.1.1'
    ],
    python_requires='>=3.6'
)