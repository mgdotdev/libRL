from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='libRL',
    version='1.0.0',
    description='Library of functions used for characterizing Microwave Absorption',
    long_description=long_description,
    url='https://github.com/1mikegrn/libRL',
    author='Michael Green',
    author_email='1mikegrn@gmail.com',

    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: STEM research',
        'License :: OSI Approved :: GPL3 License',
    ],

    packages=find_packages(),

    package_data={
        'libRL': ['*.c', '*pyd', '*pyx']
    },

    include_package_data=True,
    python_requires='>=3.7',

    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'pathos',
        'xlrd',
    ],

    project_urls={
        'GutHub': 'https://github.com/1mikegrn/libRL',
        'Website': 'http://www.inorganicexposure.com',
        'Google Scholar': 'https://scholar.google.com/citations?user=DxFljRYAAAAJ&hl=en'
    }
)