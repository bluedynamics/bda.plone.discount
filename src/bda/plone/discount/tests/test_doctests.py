from interlude import interact
from plone.testing import layered
from bda.plone.discount.tests import Discount_FIXTURE

import doctest
import os
import pprint
import unittest


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

TESTFILES = [
    ('settings.rst', Discount_FIXTURE),
    ('calculator.rst', Discount_FIXTURE)
]

def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(
                filename,
                optionflags=optionflags,
                globs={
                    'interact': interact,
                    'pprint': pprint.pprint,
                },
            ), layer=layer
        )
        for filename, layer in TESTFILES]
    )
