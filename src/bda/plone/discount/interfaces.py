# -*- coding: utf-8 -*-
from datetime import datetime
from zope.interface import Interface


FLOOR_DATETIME = datetime(2000, 1, 1, 0, 0, 0)
CEILING_DATETIME = datetime(2100, 1, 1, 0, 0, 0)
CATEGORY_CART_ITEM = 'cart_item'
CATEGORY_CART = 'cart'
FOR_USER = 'user'
FOR_GROUP = 'group'
KIND_PERCENT = 'percent'
KIND_OFF = 'off'
KIND_ABSOLUTE = 'absolute'
THRESHOLD_PRICE = 'price'
THRESHOLD_ITEM_COUNT = 'count'
ALL_PORTAL_TYPES = 'all'


class IDiscountExtensionLayer(Interface):
    """Browser layer for bda.plone.discount.
    """


class IDiscountSettingsEnabled(Interface):
    """Interface for marking content having discount settings enabled.
    """


class IDiscountSettings(Interface):
    """Interface for discount settings.
    """

    def rules(context, date=None, user='', group=''):
        """Return discount rules for context. Optional anchor ``date`` and
        ``user`` or group can be given as search criteria.
        """


class ICartItemDiscountSettings(IDiscountSettings):
    """Interface for cart item discount settings.
    """


class IUserCartItemDiscountSettings(ICartItemDiscountSettings):
    """Interface for cart item user discount settings.
    """


class IGroupCartItemDiscountSettings(ICartItemDiscountSettings):
    """Interface for cart item group discount settings.
    """


class ICartDiscountSettings(IDiscountSettings):
    """Interface for cart discount settings.
    """


class IUserCartDiscountSettings(ICartDiscountSettings):
    """Interface for cart user discount settings.
    """


class IGroupCartDiscountSettings(ICartDiscountSettings):
    """Interface for cart group discount settings.
    """
