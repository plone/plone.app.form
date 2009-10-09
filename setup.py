from setuptools import setup, find_packages

version = '1.1.9'

setup(name='plone.app.form',
      version=version,
      description="zope.formlib integration for Plone",
      long_description="""\
This package enables zope.formlib forms to work in Zope 2 code, styled to
look like Plone forms. Note that developers should use zope.formlib directly,
not Products.Five.formlib.
""",
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.form',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      )
