import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="billing_2",
    version="0.0.2",
    author="Danila",
    author_email="danilamgallo@gmail.com",
    description=("Billing module test 2"),
    license="BSD",
    keywords="billing invoice",
    url="http://project.billing_module.com",
    packages=['billing_module', 'tests'],
    long_description=read('README.md'),
    python_requires='>=3.6',
)
