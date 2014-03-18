from zope.interface import implementer
from zope.component import adapter
from Products.CMFPlone.interfaces import IPloneSiteRoot
from bda.plone.discount.interfaces import IDiscountEnabled
from bda.plone.discount.interfaces import IDiscountSettings
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings


@implementer(IDiscountSettings)
class PersistendDiscountSettings(object):

    def __init__(self, context):
        self.context = context


@implementer(ICartItemDiscountSettings)
class CartItemDiscountSettings(PersistendDiscountSettings):
    pass


@implementer(IUserCartItemDiscountSettings)
class UserCartItemDiscountSettings(CartItemDiscountSettings):
    pass


@implementer(IGroupCartItemDiscountSettings)
class GroupCartItemDiscountSettings(CartItemDiscountSettings):
    pass


@implementer(ICartDiscountSettings)
@adapter(IPloneSiteRoot)
class CartDiscountSettings(PersistendDiscountSettings):
    pass


@implementer(IUserCartDiscountSettings)
@adapter(IPloneSiteRoot)
class UserCartDiscountSettings(CartDiscountSettings):
    pass


@implementer(IGroupCartDiscountSettings)
@adapter(IPloneSiteRoot)
class GroupCartDiscountSettings(CartDiscountSettings):
    pass
