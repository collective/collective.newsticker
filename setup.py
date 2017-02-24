# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.0rc2.dev0'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.newsticker',
    version=version,
    description='News ticker inspired by the one on the BBC News website.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone jquery news ticker',
    author='Héctor Velarde',
    author_email='hector.velarde@gmail.com',
    url='https://github.com/collective/collective.newsticker',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.layout',
        'plone.app.registry',
        'plone.registry',
        'Products.CMFPlone >=4.2',
        'Products.GenericSetup',
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'lxml',
            'plone.app.robotframework',  # required by plone.app.event
            'plone.app.testing',
            'plone.browserlayer',
            'zope.viewlet',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
