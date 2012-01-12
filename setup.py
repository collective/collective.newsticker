# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0dev'

setup(name='collective.newsticker',
      version=version,
      description="An implementation of the jQuery News Ticker Plugin for Plone.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                       open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone :: 4.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone jquery newsticker',
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.newsticker',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.grok>=1.2.0',
        'zope.schema>=3.8.0',  # required to use IContextAwareDefaultFactory
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
