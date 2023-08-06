import pathlib

import setuptools


setuptools.setup(
    author='Michael Vartanyan',
    author_email='mv@spherical.pm',
    description='Plugin generate tree data structure from your flat menu model',
    keywords='Lektor plugin tree menu',
    license='MIT',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    name='lektor-treeify',
    packages=setuptools.find_packages(),
    py_modules=['lektor_treeify'],
    version='1.2',
    install_requires=[
        'more_itertools',
        'simplejson',
    ],
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    extras_require={
        'dev': [
            'spherical-dev[dev]>0.0.2',
        ],
    },
    entry_points={
        'lektor.plugins': [
            'treeify = lektor_treeify:TreeifyPlugin',
        ],
    },
)
