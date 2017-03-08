Settings
========

Imports:

.. code-block:: pycon

    >>> from bda.plone.discount.interfaces import ICartDiscountSettings
    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IDiscountSettingsEnabled
    >>> from bda.plone.discount.interfaces import IGroupCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartDiscountSettings
    >>> from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
    >>> from bda.plone.discount.interfaces import KIND_ABSOLUTE
    >>> from bda.plone.discount.interfaces import KIND_OFF
    >>> from bda.plone.discount.interfaces import KIND_PERCENT
    >>> from datetime import datetime
    >>> from node.utils import UNSET
    >>> from zope.interface import alsoProvides

Get portal from layer:

.. code-block:: pycon

    >>> plone = layer['portal']

Debug print helper:

.. code-block:: pycon

    >>> def print_rule(rule):
    ...     print 'index: ' + str(rule.attrs['index'])
    ...     print 'category: ' + str(rule.attrs['category'])
    ...     print 'context_uid: ' + str(rule.attrs['context_uid'])
    ...     print 'creator: ' + rule.attrs['creator']
    ...     print 'created: ' + str(rule.attrs['created'])
    ...     print 'kind: ' + rule.attrs['kind']
    ...     print 'block: ' + str(rule.attrs['block'])
    ...     print 'value: ' + str(rule.attrs['value'])
    ...     print 'threshold: ' + str(rule.attrs['threshold'])
    ...     print 'threshold_calculation: ' + str(rule.attrs['threshold_calculation'])
    ...     print 'portal_type: ' + str(rule.attrs['portal_type'])
    ...     print 'valid_from: ' + str(rule.attrs['valid_from'])
    ...     print 'valid_to: ' + str(rule.attrs['valid_to'])
    ...     print 'user: ' + rule.attrs['user']
    ...     print 'group: ' + rule.attrs['group']


ICartItemDiscountSettings
-------------------------

.. code-block:: pycon

    >>> settings = ICartItemDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.CartItemDiscountSettings object at ...>

Add some rules:

.. code-block:: pycon

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET)

    >>> settings.add_rule(context=plone, index=1, kind=KIND_OFF,
    ...                   block=False, value=1.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=datetime(2014, 2, 1, 0, 0, 0),
    ...                   valid_to=datetime(2014, 4, 1, 0, 0, 0))

    >>> settings.add_rule(context=plone, index=2, kind=KIND_ABSOLUTE,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=datetime(2014, 1, 1, 0, 0, 0),
    ...                   valid_to=datetime(2014, 3, 1, 0, 0, 0))

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    3

Look at rule data:

.. code-block:: pycon

    >>> print_rule(rules[0])
    index: 1
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: off
    block: False
    value: 1.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2014-02-01 00:00:00
    valid_to: 2014-04-01 00:00:00
    user: 
    group: 

Rules are returned sorted by valid_from, most recent first:

.. code-block:: pycon

    >>> rules[1].attrs['valid_from']
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> rules[1].attrs['valid_to']
    datetime.datetime(2014, 3, 1, 0, 0)

    >>> rules[2].attrs['valid_from']
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> rules[2].attrs['valid_to']
    datetime.datetime(2100, 1, 1, 0, 0)

Anchor rule lookup by date, which must be between valid_from and valid_to:

.. code-block:: pycon

    >>> rules = [_ for _ in settings.rules(
    ...          plone, date=datetime(2013, 12, 1, 0, 0, 0))]
    >>> len(rules)
    1

    >>> rules[0].attrs['valid_from']
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> rules[0].attrs['valid_to']
    datetime.datetime(2100, 1, 1, 0, 0)

    >>> rules = [_ for _ in settings.rules(
    ...          plone, date=datetime(2014, 1, 15, 0, 0, 0))]
    >>> len(rules)
    2

    >>> rules[0].attrs['valid_from']
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> rules[0].attrs['valid_to']
    datetime.datetime(2014, 3, 1, 0, 0)
    >>> rules[1].attrs['valid_from']
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> rules[1].attrs['valid_to']
    datetime.datetime(2100, 1, 1, 0, 0)

    >>> rules = [_ for _ in settings.rules(
    ...          plone, date=datetime(2014, 2, 15, 0, 0, 0))]
    >>> len(rules)
    3

    >>> rules[0].attrs['valid_from']
    datetime.datetime(2014, 2, 1, 0, 0)
    >>> rules[0].attrs['valid_to']
    datetime.datetime(2014, 4, 1, 0, 0)
    >>> rules[1].attrs['valid_from']
    datetime.datetime(2014, 1, 1, 0, 0)
    >>> rules[1].attrs['valid_to']
    datetime.datetime(2014, 3, 1, 0, 0)
    >>> rules[2].attrs['valid_from']
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> rules[2].attrs['valid_to']
    datetime.datetime(2100, 1, 1, 0, 0)

    >>> rules = [_ for _ in settings.rules(
    ...          plone, date=datetime(2014, 3, 15, 0, 0, 0))]
    >>> len(rules)
    2

    >>> rules[0].attrs['valid_from']
    datetime.datetime(2014, 2, 1, 0, 0)
    >>> rules[0].attrs['valid_to']
    datetime.datetime(2014, 4, 1, 0, 0)
    >>> rules[1].attrs['valid_from']
    datetime.datetime(2000, 1, 1, 0, 0)
    >>> rules[1].attrs['valid_to']
    datetime.datetime(2100, 1, 1, 0, 0)


IUserCartItemDiscountSettings
-----------------------------

.. code-block:: pycon

    >>> settings = IUserCartItemDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.UserCartItemDiscountSettings object at ...>

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, user='max')

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    1

    >>> print_rule(rules[0])
    index: 0
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2000-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: max
    group: 


IGroupCartItemDiscountSettings
------------------------------

.. code-block:: pycon

    >>> settings = IGroupCartItemDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.GroupCartItemDiscountSettings object at ...>

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, group='retailer')

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    1

    >>> print_rule(rules[0])
    index: 0
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2000-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: 
    group: retailer


ICartDiscountSettings
---------------------

.. code-block:: pycon

    >>> settings = ICartDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.CartDiscountSettings object at ...>

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET)

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    1

    >>> print_rule(rules[0])
    index: 0
    category: cart
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2000-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: 
    group: 


IUserCartDiscountSettings
-------------------------

.. code-block:: pycon

    >>> settings = IUserCartDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.UserCartDiscountSettings object at ...>

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET, user='sepp')

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    1

    >>> print_rule(rules[0])
    index: 0
    category: cart
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2000-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: sepp
    group: 


IGroupCartDiscountSettings
--------------------------

.. code-block:: pycon

    >>> settings = IGroupCartDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.GroupCartDiscountSettings object at ...>

    >>> settings.add_rule(context=plone, index=0, kind=KIND_PERCENT,
    ...                   block=False, value=10.0, threshold=UNSET,
    ...                   threshold_calculation=UNSET, portal_type=UNSET,
    ...                   valid_from=UNSET, valid_to=UNSET,
    ...                   group='master_dealer')

    >>> rules = [_ for _ in settings.rules(plone)]
    >>> len(rules)
    1

    >>> print_rule(rules[0])
    index: 0
    category: cart
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    threshold_calculation: 
    portal_type: 
    valid_from: 2000-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: 
    group: master_dealer


IDiscountSettingsEnabled
------------------------

.. code-block:: pycon

    >>> _ = plone.invokeFactory("Folder", "folder")
    >>> _ = plone.folder.invokeFactory("Folder", "subfolder")
    >>> alsoProvides(plone.folder.subfolder, IDiscountSettingsEnabled)

    >>> IDiscountSettingsEnabled.providedBy(plone.folder)
    False

    >>> IDiscountSettingsEnabled.providedBy(plone.folder.subfolder)
    True

    >>> folder = plone.folder.subfolder
    >>> folder
    <...Folder at /plone/folder/subfolder>

    >>> ICartItemDiscountSettings(folder)
    <bda.plone.discount.settings.CartItemDiscountSettings object at ...>

    >>> IUserCartItemDiscountSettings(folder)
    <bda.plone.discount.settings.UserCartItemDiscountSettings object at ...>

    >>> IGroupCartItemDiscountSettings(folder)
    <bda.plone.discount.settings.GroupCartItemDiscountSettings object at ...>

    >>> ICartDiscountSettings(folder)
    Traceback (most recent call last):
      ...
    TypeError: ...

    >>> ICartItemDiscountSettings(plone.folder)
    Traceback (most recent call last):
      ...
    TypeError: ...

    >>> ICartDiscountSettings(plone.folder)
    Traceback (most recent call last):
      ...
    TypeError: ...


Cleanup
-------

Overall rules in soup:

.. code-block:: pycon

    >>> len(settings.rules_soup.storage)
    8

    >>> settings.rules_soup.clear()
