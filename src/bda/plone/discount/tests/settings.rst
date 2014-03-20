Settings
========

::

    >>> plone = layer['portal']

    >>> from bda.plone.discount.interfaces import ICartItemDiscountSettings
    >>> ICartItemDiscountSettings(plone)
    <bda.plone.discount.settings.CartItemDiscountSettings object at ...>

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
