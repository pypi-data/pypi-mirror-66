# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:02:48 2020

@author: shriy
"""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='web_and_file_utils',
    version='0.1.3',
    description='Useful web and file utilities in Python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author='Shriya Das',
    author_email='shriya2017das@gmail.com',
    keywords=['Web Utilities', 'File Utilities', 'URL Status Checker', 'File Fetching'],
    url='https://github.com/Shriya99/web_and_file_utils',
)



if __name__ == '__main__':
    setup(**setup_args)