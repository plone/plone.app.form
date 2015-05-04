# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '2.3.2'

long_description = (open("README.rst").read() + "\n" +
                    open("CHANGES.rst").read())

setup(name='plone.app.form',
      version=version,
      description="zope.formlib integration for Plone",
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
      ],
      keywords='plone form formlib',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.form',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'plone.app.content',
              'plone.app.testing',
              'plone.memoize',
              'zope.annotation',
              'zope.publisher',
              'zope.testing',
          ],
      ),
      install_requires=[
          'Acquisition',
          'DateTime',
          'five.formlib',
          'plone.app.vocabularies',
          'plone.locking',
          'Products.CMFCore',
          'Products.CMFDefault',
          'setuptools',
          'zope.browser',
          'zope.component',
          'zope.event',
          'zope.formlib >= 4.0',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
          'zope.site',
          'Zope2 >= 2.12.3',
      ],
      )
