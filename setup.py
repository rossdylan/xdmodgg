from setuptools import setup, find_packages

requires = [
    'requests'
]

setup(
    name='xdmodgg',
    version='0.1.0',
    description='A tool to download graphs from xdmod',
    author='Ross Delinger',
    author_email='rossdylan@csh.rit.edu',
    packages=find_packages(),
    install_requires=requires,
    zip_safe=False,
)
