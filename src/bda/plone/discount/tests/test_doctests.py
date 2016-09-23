# -*- coding: utf-8 -*-
from bda.plone.discount.tests import Discount_INTEGRATION_TESTING
from interlude import interact
from plone.testing import layered
from plone.testing import z2

import doctest
import pprint
import unittest


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


TESTFILES = [
    'settings.rst',
    'calculator.rst',
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                globs={'interact': interact,
                       'pprint': pprint.pprint,
                       'z2': z2,
                       },
                optionflags=optionflags,
            ),
            layer=Discount_INTEGRATION_TESTING,
        )
        for docfile in TESTFILES
    ])
    return suite
