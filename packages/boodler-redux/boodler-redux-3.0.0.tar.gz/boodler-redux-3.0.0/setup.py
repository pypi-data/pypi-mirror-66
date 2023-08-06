#!/usr/bin/env python

from setuptools import Extension, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='boodler-redux',
    version='3.0.0',
    description='A programmable soundscape tool',
    author='Beau Gunderson',
    author_email='beau@beaugunderson.com',
    url='https://github.com/beaugunderson/boodler-redux',
    license='GNU LGPL',
    platforms=['MacOS X', 'POSIX'],
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio :: Mixers',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: GNU Library or '
         'Lesser General Public License (LGPL)'),
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'packaging',
    ],
    tests_require=[
        'tox',
    ],
    packages=[
        'boodle',
        'booman',
        'boopak',
    ],
    package_dir={
        'boodle': 'src/boodle',
        'booman': 'src/booman',
        'boopak': 'src/boopak',
    },
    scripts=[
        'script/boodler',
        'script/boodle-mgr',
        'script/boodle-event',
    ],
    ext_modules=[
        Extension(
            'boodle.cboodle_stdout',
            [
                'src/cboodle/audev-stdout.c',
                'src/cboodle/cboodle-stdout.c',
                'src/cboodle/noteq.c',
                'src/cboodle/sample.c',
            ]
        ),
    ],
)
