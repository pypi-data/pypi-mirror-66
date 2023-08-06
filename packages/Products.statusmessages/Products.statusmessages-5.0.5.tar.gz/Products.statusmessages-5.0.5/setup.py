# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '5.0.5'

setup(
    name='Products.statusmessages',
    version=version,
    description='statusmessages provides an easy way of handling '
                'internationalized status messages managed via an '
                'BrowserRequest adapter storing status messages in '
                'client-side cookies.',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Framework :: Plone :: Core',
        'Framework :: Zope2',
        'Framework :: Zope :: 4',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Zope CMF Plone status messages i18n',
    author='Hanno Schlichting',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/Products.statusmessages',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'zope.component',
            'Zope2',
        ],
    ),
    install_requires=[
        'setuptools',
        'six',
        'zope.annotation',
        'zope.i18n',
        'zope.interface',
    ],
)
