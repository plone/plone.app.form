from setuptools import setup, find_packages
import sys, os

version = '1.0a2'

setup(name='plone.app.form',
      version=version,
      description="Form integration for Plone",
      long_description="""\
This package enables zope.formlib forms to work in Zope 2 code, styled to
look like Plone forms. Note that developers should use zope.formlib directly,
not Products.Five.formlib.
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Framework :: Zope2'],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.app.form',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )