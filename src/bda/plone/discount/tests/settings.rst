Settings
========

::

    >>> plone = layer['portal']

    >>> def print_role(role):
    ...     print 'index: ' + str(role.attrs['index'])
    ...     print 'category: ' + str(role.attrs['category'])
    ...     print 'context_uid: ' + str(role.attrs['context_uid'])
    ...     print 'creator: ' + role.attrs['creator']
    ...     print 'created: ' + str(role.attrs['created'])
    ...     print 'kind: ' + role.attrs['kind']
    ...     print 'block: ' + str(role.attrs['block'])
    ...     print 'value: ' + str(role.attrs['value'])
    ...     print 'threshold: ' + str(role.attrs['threshold'])
    ...     print 'valid_from: ' + str(role.attrs['valid_from'])
    ...     print 'valid_to: ' + str(role.attrs['valid_to'])
    ...     print 'user: ' + role.attrs['user']
    ...     print 'group: ' + role.attrs['group']

    >>> from datetime import datetime
    >>> from node.utils import UNSET

    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> settings = ICartItemDiscountSettings(plone)
    >>> settings
    <bda.plone.discount.settings.CartItemDiscountSettings object at ...>

    >>> settings.add_rule(
    ...     plone, 0, 'percent', False, 10.0, UNSET, UNSET, UNSET)

    >>> settings.add_rule(
    ...     plone, 1, 'off', False, 1.0, UNSET,
    ...     datetime(2014, 2, 1, 0, 0, 0), datetime(2014, 4, 1, 0, 0, 0))

    >>> settings.add_rule(
    ...     plone, 2, 'absolute', False, 10.0, UNSET,
    ...     datetime(2014, 1, 1, 0, 0, 0), datetime(2014, 3, 1, 0, 0, 0))

    >>> roles = [_ for _ in settings.rules(plone)]
    >>> len(roles)
    3

    >>> print_role(roles[0])
    index: 1
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: off
    block: False
    value: 1.0
    threshold: 
    valid_from: 2014-02-01 00:00:00
    valid_to: 2014-04-01 00:00:00
    user: 
    group: 

    >>> print_role(roles[1])
    index: 2
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: absolute
    block: False
    value: 10.0
    threshold: 
    valid_from: 2014-01-01 00:00:00
    valid_to: 2014-03-01 00:00:00
    user: 
    group: 

    >>> print_role(roles[2])
    index: 0
    category: cart_item
    context_uid: 77c4390d-1179-44ba-9d57-46d23ac292c6
    creator: test_user_1_
    created: ...
    kind: percent
    block: False
    value: 10.0
    threshold: 
    valid_from: 1970-01-01 00:00:00
    valid_to: 2100-01-01 00:00:00
    user: 
    group: 

    >>> from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
    >>> IUserCartItemDiscountSettings(plone)
    <bda.plone.discount.settings.UserCartItemDiscountSettings object at ...>

    >>> from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
    >>> IGroupCartItemDiscountSettings(plone)
    <bda.plone.discount.settings.GroupCartItemDiscountSettings object at ...>

    >>> from bda.plone.discount.interfaces import ICartDiscountSettings
    >>> ICartDiscountSettings(plone)
    <bda.plone.discount.settings.CartDiscountSettings object at ...>

    >>> from bda.plone.discount.interfaces import IUserCartDiscountSettings
    >>> IUserCartDiscountSettings(plone)
    <bda.plone.discount.settings.UserCartDiscountSettings object at ...>

    >>> from bda.plone.discount.interfaces import IGroupCartDiscountSettings
    >>> IGroupCartDiscountSettings(plone)
    <bda.plone.discount.settings.GroupCartDiscountSettings object at ...>

    >>> from zope.interface import alsoProvides
    >>> from bda.plone.discount.interfaces import IDiscountSettingsEnabled

    >>> _ = plone.invokeFactory("Folder", "folder")
    >>> _ = plone.folder.invokeFactory("Folder", "subfolder")
    >>> alsoProvides(plone.folder.subfolder, IDiscountSettingsEnabled)

    >>> IDiscountSettingsEnabled.providedBy(plone.folder)
    False

    >>> IDiscountSettingsEnabled.providedBy(plone.folder.subfolder)
    True

    >>> folder = plone.folder.subfolder
    >>> folder
    <ATFolder at /plone/folder/subfolder>

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
