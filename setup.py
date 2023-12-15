# coding=utf-8

import re
from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the version string
with open(path.join(here, 'promptcraft/__init__.py'), encoding='utf-8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='promptcraft',
    version=version,
    description='PromptCraft: A Prompt Perturbation Toolkit for Prompt Robustness Analysis',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/SuperBruceJia/promptcraft',
    author='Shuyue Jia',
    author_email='shuyuej@ieee.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Prompt Perturbation',
    package_data={"":["*.py"]},
    packages=["promptcraft"],
    include_package_data=True,
    install_requires=['torch',
                      'bitsandbytes',
                      'transformers',
                      'pandas',
                      'Levenshtein',
                      'scipy',
                      'sklearn_pandas',
                      'scikit-learn',
                      'sentence_transformers',
                      'googletrans==3.1.0a0',
                      'nltk',
                      'sacremoses',
                      'sentencepiece',
                      ]
)
