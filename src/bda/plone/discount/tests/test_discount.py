import unittest2 as unittest
from zope.component import provideAdapter
from zope.interface import Interface
from plone.uuid.interfaces import IUUID
from bda.plone.discount import UUID_PLONE_ROOT
from bda.plone.discount.tests import Discount_INTEGRATION_TESTING
from bda.plone.discount.tests import set_browserlayer


class TestDiscount(unittest.TestCase):
    layer = Discount_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_plone_root_uuid(self):
        self.assertEquals(IUUID(self.portal), UUID_PLONE_ROOT)
