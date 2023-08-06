#!/usr/bin/env python

"""The setup script."""
import os

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]
setup(
    author="Yoni Mood",
    author_email='yonimdo@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    description=read('readme.md'),
    entry_points={
        'console_scripts': [
            'rain = {0}:main'.format(read('version').split(':')[0])
        ],
    },
    install_requires=read('requirements.txt').split('\n'),
    license="BSD license",
    long_description=read('readme.md'),
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='''rain_api, apis,
                downdload api from the internet, rain api, rain start''',
    name='rain_api',
    packages=find_packages(include=['*', 'rain_api', 'rain_api.*' '*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/yonimdo/rain_api',
    version=read('version').split(':')[1],
    zip_safe=False,
)
