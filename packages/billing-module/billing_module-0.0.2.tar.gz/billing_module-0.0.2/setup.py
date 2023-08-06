import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="billing_module",
    version="0.0.2",
    author="Danila",
    author_email="danilamgallo@gmail.com",
    description="Billing module",
    license="BSD",
    keywords="billing invoice",
    url="https://github.com/danilagallo",
    packages=['billing_module', 'tests'],
    long_description=read('README.md'),
    python_requires='>=3.6',
)
