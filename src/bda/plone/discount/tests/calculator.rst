Calculator
==========

::

    >>> from datetime import datetime
    >>> from node.utils import UNSET
    >>> plone = layer['portal']

Import settings related interfaces::

    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import ICartDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartDiscountSettings


RuleLookup
----------

Import rules lookup implementations::

    >>> from bda.plone.discount.calculator import ItemRulesLookup
    >>> from bda.plone.discount.calculator import UserItemRulesLookup
    >>> from bda.plone.discount.calculator import GroupItemRulesLookup
    >>> from bda.plone.discount.calculator import CartRulesLookup
    >>> from bda.plone.discount.calculator import UserCartRulesLookup
    >>> from bda.plone.discount.calculator import GroupCartRulesLookup

Test lookup objects::

    >>> date = datetime(2014, 1, 1)
    >>> ItemRulesLookup(plone, date).lookup()

    >>> settings = ICartItemDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 5.0, UNSET, UNSET, UNSET)

    >>> ItemRulesLookup(plone, date).lookup()
    <Record object 'None' at ...>

    >>> settings = IUserCartItemDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 10.0, UNSET, UNSET, UNSET, user='usr1')

    >>> UserItemRulesLookup(plone, date, for_value='usr1').lookup()
    <Record object 'None' at ...>

    >>> UserItemRulesLookup(plone, date, for_value='usr2').lookup()

    >>> settings = IGroupCartItemDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 15.0, UNSET, UNSET, UNSET, group='grp1')

    >>> GroupItemRulesLookup(plone, date, for_value='grp1').lookup()
    <Record object 'None' at ...>

    >>> GroupItemRulesLookup(plone, date, for_value='grp2').lookup()

    >>> settings = ICartDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 20.0, UNSET, UNSET, UNSET)

    >>> CartRulesLookup(plone, date).lookup()
    <Record object 'None' at ...>

    >>> settings = IUserCartDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 25.0, UNSET, UNSET, UNSET, user='usr2')

    >>> UserCartRulesLookup(plone, date, for_value='usr1').lookup()

    >>> UserCartRulesLookup(plone, date, for_value='usr2').lookup()
    <Record object 'None' at ...>

    >>> settings = IGroupCartDiscountSettings(plone)
    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 30.0, UNSET, UNSET, UNSET, group='grp2')

    >>> GroupCartRulesLookup(plone, date, for_value='grp1').lookup()

    >>> GroupCartRulesLookup(plone, date, for_value='grp2').lookup()
    <Record object 'None' at ...>


RuleAcquierer
-------------

Import rule acquirer implementations::

    >>> from bda.plone.discount.calculator import CartItemRuleAcquirer
    >>> from bda.plone.discount.calculator import CartRuleAcquirer