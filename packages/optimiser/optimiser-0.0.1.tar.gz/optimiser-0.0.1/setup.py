"""
Just a regular `setup.py` file.

Author: Nikolay Lysenko
"""


import os
from setuptools import setup, find_packages


current_dir = os.path.abspath(os.path.dirname(__file__))

description = 'Generic implementations of some numeric optimization methods.'
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='optimiser',
    version='0.0.1',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nikolay-Lysenko/optimiser',
    author='Nikolay Lysenko',
    author_email='nikolay-lysenco@yandex.ru',
    license='MIT',
    keywords=[
        'blackbox_optimization',
        'numeric_optimization',
        'crossentropy'
    ],
    packages=find_packages(),
    package_data={},
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
