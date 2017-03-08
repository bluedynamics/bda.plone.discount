Calculator
==========

Imports:

.. code-block:: pycon

    >>> from bda.plone.discount.calculator import CartItemRuleAcquirer
    >>> from bda.plone.discount.calculator import CartRuleAcquirer
    >>> from bda.plone.discount.calculator import CartRulesLookup
    >>> from bda.plone.discount.calculator import DiscountBase
    >>> from bda.plone.discount.calculator import GroupCartRulesLookup
    >>> from bda.plone.discount.calculator import GroupItemRulesLookup
    >>> from bda.plone.discount.calculator import ItemRulesLookup
    >>> from bda.plone.discount.calculator import UserCartRulesLookup
    >>> from bda.plone.discount.calculator import UserItemRulesLookup
    >>> from bda.plone.discount.interfaces import ICartDiscountSettings
    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import KIND_PERCENT
    >>> from bda.plone.discount.settings import create_rule
    >>> from datetime import datetime
    >>> from node.utils import UNSET

Get portal from layer:

.. code-block:: pycon

    >>> plone = layer['portal']


RuleLookup
----------

Test lookup objects:

.. code-block:: pycon

    >>> date = datetime(2014, 1, 1)
    >>> ItemRulesLookup(plone, date).lookup()

    >>> settings = ICartItemDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=5.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET)

    >>> ItemRulesLookup(plone, date).lookup()
    <Record object 'None' at ...>

    >>> settings = IUserCartItemDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, user='usr1')

    >>> UserItemRulesLookup(plone, date, for_value='usr1').lookup()
    <Record object 'None' at ...>

    >>> UserItemRulesLookup(plone, date, for_value='usr2').lookup()

    >>> settings = IGroupCartItemDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=15.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, group='grp1')

    >>> GroupItemRulesLookup(plone, date, for_value='grp1').lookup()
    <Record object 'None' at ...>

    >>> GroupItemRulesLookup(plone, date, for_value='grp2').lookup()

    >>> settings = ICartDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=20.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET)

    >>> CartRulesLookup(plone, date).lookup()
    <Record object 'None' at ...>

    >>> settings = IUserCartDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=25.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, user='usr2')

    >>> UserCartRulesLookup(plone, date, for_value='usr1').lookup()

    >>> UserCartRulesLookup(plone, date, for_value='usr2').lookup()
    <Record object 'None' at ...>

    >>> settings = IGroupCartDiscountSettings(plone)
    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=30.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, group='grp2')

    >>> GroupCartRulesLookup(plone, date, for_value='grp1').lookup()

    >>> GroupCartRulesLookup(plone, date, for_value='grp2').lookup()
    <Record object 'None' at ...>


DiscountBase
------------

Prepare:

.. code-block:: pycon

    >>> class TestRuleAcquirer(object):
    ...     rules = list()

    >>> acquirer = TestRuleAcquirer()

    >>> class TestDiscount(DiscountBase):
    ...     acquirer = acquirer

Test rule application:

.. code-block:: pycon

    >>> discount = TestDiscount(plone)
