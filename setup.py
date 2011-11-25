# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0dev'

setup(name='collective.newsticker',
      version=version,
      description="An implementation of the jQuery News Ticker Plugin for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Plone :: 4.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        ],
      keywords='plone jquery',
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
        'five.grok',
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
