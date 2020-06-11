from setuptools import setup, find_packages
from os import path

here = path.dirname(path.abspath(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='libRL',
    version='1.2.0 α',
    description='Python library for characterizing Microwave Absorption',
    long_description=long_description,
    url='https://github.com/1mikegrn/libRL',
    author='Michael Green',
    author_email='1mikegrn@gmail.com',
    license='GPL-3.0',

    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: STEM research',
        'License :: OSI Approved :: GPL-3.0 License',
    ],

    packages=find_packages(),

    include_package_data=True,

    python_requires='>=3.6',

    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'pathos',
        'xlrd',
        'openpyxl',
        'matplotlib',
        'flask',
    ],

    entry_points={
        'console_scripts': ['libRL-app=libRL.app:init']
    },

    project_urls={
        'GitHub': 'https://github.com/1mikegrn/libRL',
        'DocSite': 'https://1mikegrn.github.io/libRL/',
        'Personal Webpage': 'https://1mikegrn.github.io',
        'Google Scholar': 'https://scholar.google.com/citations?user=DxFljRYAAAAJ&hl=en'
    }
)