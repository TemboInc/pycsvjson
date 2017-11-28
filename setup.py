import os
from setuptools import setup, find_packages
from pycsvjson.pycsvjson import __version__ as VERSION


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('REQUIREMENTS').splitlines()
tests_requirements = read('REQUIREMENTS-TESTS').splitlines()

setup(
    name="pycsvjson",
    version=VERSION,
    description="A utility to transform CSV files into structured JSON",
    long_description=read('README.md'),
    url='https://github.com/TemboInc/pycsvjson',
    license='MIT License',
    author='Tembo Inc.',
    author_email='devsupport@temboinc.com',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requirements,
    tests_require=tests_requirements,
    entry_points = {
        'console_scripts': [
            'pycsvjson=pycsvjson.pycsvjson:main',
        ],
    },
)
