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
    >>> from bda.plone.discount.interfaces import ALL_PORTAL_TYPES
    >>> from bda.plone.discount.interfaces import CATEGORY_CART_ITEM
    >>> from bda.plone.discount.interfaces import ICartDiscountSettings
    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import KIND_ABSOLUTE
    >>> from bda.plone.discount.interfaces import KIND_PERCENT
    >>> from bda.plone.discount.interfaces import KIND_OFF
    >>> from bda.plone.discount.interfaces import THRESHOLD_PRICE
    >>> from bda.plone.discount.interfaces import THRESHOLD_ITEM_COUNT
    >>> from bda.plone.discount.settings import create_rule
    >>> from datetime import datetime
    >>> from decimal import Decimal
    >>> from node.utils import UNSET
    >>> import uuid

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

Test rule application:

.. code-block:: pycon

    >>> class TestDiscount(DiscountBase):
    ...     acquirer = None

    >>> discount = TestDiscount(plone)

Rule always applies, no threshold, discount calculation by percent:

.. code-block:: pycon

    >>> rule = create_rule(
    ...     uid=uuid.uuid4(), category=CATEGORY_CART_ITEM, creator='admin',
    ...     index=0, kind=KIND_PERCENT, block=False, value=10.0,
    ...     threshold=UNSET, threshold_calculation=THRESHOLD_PRICE,
    ...     portal_type=UNSET, valid_from=UNSET, valid_to=UNSET)

    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(1))
    Decimal('9.0')

    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(3))
    Decimal('9.0')

Threshold by price, applies as of total items price 20.0:

.. code-block:: pycon

    >>> rule.attrs['threshold'] = 20.0
    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(1))
    Decimal('10.0')

    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(2))
    Decimal('9.0')

Threshold by item count, applies as of 2 items:

.. code-block:: pycon

    >>> rule.attrs['threshold'] = 2.0
    >>> rule.attrs['threshold_calculation'] = THRESHOLD_ITEM_COUNT
    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(1))
    Decimal('10.0')

    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal(2))
    Decimal('9.0')

Rule application by portal type. Rule Applies to all portal types:

.. code-block:: pycon

    >>> rule.attrs['threshold'] = UNSET
    >>> rule.attrs['threshold_calculation'] = THRESHOLD_PRICE
    >>> rule.attrs['portal_type'] = ALL_PORTAL_TYPES
    >>> discount.apply_rule(Decimal('10.0'), rule, portal_type='My Type')
    Decimal('9.0')

Rule Applies to ``My Type``:

.. code-block:: pycon

    >>> rule.attrs['portal_type'] = 'My Type'
    >>> discount.apply_rule(Decimal('10.0'), rule, portal_type='Other Type')
    Decimal('10.0')

    >>> discount.apply_rule(Decimal('10.0'), rule, portal_type='My Type')
    Decimal('9.0')

Discount calculation as value reduced from price:

.. code-block:: pycon

    >>> rule.attrs['portal_type'] = ALL_PORTAL_TYPES
    >>> rule.attrs['kind'] = KIND_OFF
    >>> rule.attrs['value'] = 3.0
    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal('5.0'))
    Decimal('7.0')

Discount calculation as absolute new price:

.. code-block:: pycon

    >>> rule.attrs['kind'] = KIND_ABSOLUTE
    >>> rule.attrs['value'] = 5.5
    >>> discount.apply_rule(Decimal('10.0'), rule, count=Decimal('5.0'))
    Decimal('5.5')

Test applying multiple rules. First rule discounts 10%, second reduces price by
1:

.. code-block:: pycon

    >>> class TestRuleAcquirer(object):
    ... 
    ...     def __init__(self, rules):
    ...         self._rules = rules
    ... 
    ...     def rules(self, portal_type=None):
    ...         return self._rules

    >>> rule_1 = create_rule(
    ...     uid=uuid.uuid4(), category=CATEGORY_CART_ITEM, creator='admin',
    ...     index=0, kind=KIND_PERCENT, block=False, value=10.0,
    ...     threshold=UNSET, threshold_calculation=THRESHOLD_PRICE,
    ...     portal_type=UNSET, valid_from=UNSET, valid_to=UNSET)

    >>> rule_2 = create_rule(
    ...     uid=uuid.uuid4(), category=CATEGORY_CART_ITEM, creator='admin',
    ...     index=1, kind=KIND_OFF, block=False, value=1.0, threshold=UNSET,
    ...     threshold_calculation=THRESHOLD_PRICE, portal_type=UNSET,
    ...     valid_from=UNSET, valid_to=UNSET)

    >>> discount.acquirer = TestRuleAcquirer([rule_1, rule_2])

    >>> discount.apply_rules(Decimal('10.0'))
    Decimal('8.0')

    >>> discount.apply_rules(Decimal('10.0'), count=Decimal('5.0'))
    Decimal('8.0')
