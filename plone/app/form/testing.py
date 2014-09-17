# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.Five
        import Products.CMFCore
        import plone.app.form
        self.loadZCML(package=Products.Five)
        self.loadZCML(package=Products.CMFCore, name='permissions.zcml')
        self.loadZCML(package=plone.app.form)

    def setUpPloneSite(self, portal):
        pass

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='plone.app.form:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='plone.app.form:Functional')
