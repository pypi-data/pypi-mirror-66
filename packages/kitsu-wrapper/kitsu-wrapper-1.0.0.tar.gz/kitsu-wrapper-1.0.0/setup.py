import re

from setuptools import setup


with open('kitsu/__init__.py', encoding='utf-8') as f:
    VERSION = re.search(r'^__version__\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']$', f.read(), re.MULTILINE).group(1)

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.rst', encoding='utf-8') as f:
    README_RST = f.read()

setup(
    name='kitsu-wrapper',
    author='Naegin',
    url='https://github.com/DiscoMusic/kitsu-wrapper',
    version=VERSION,
    packages=['kitsu'],
    install_requires=REQUIREMENTS,
    description='A simple python async wrapper for the Kitsu.io API.',
    long_description=README_RST,
    license='MIT License',
    keywords=['anime', 'manga', 'search', 'kitsu', 'api', 'wrapper'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
