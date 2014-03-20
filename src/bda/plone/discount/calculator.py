from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter
from bda.plone.cart.interfaces import ICartItem
from bda.plone.cart.interfaces import ICartDiscount
from bda.plone.cart.interfaces import ICartItemDiscount
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings


class DiscountBase(object):

    def __init__(self, context):
        self.context = context

    def aggregated_rules(self):
        pass


@implementer(ICartDiscount)
@adapter(Interface)
class CartDiscount(DiscountBase):

    def net(self, items):
        return 0.0

    def vat(self, items):
        return 0.0


@implementer(ICartItemDiscount)
@adapter(ICartItem)
class CartItemDiscount(DiscountBase):

    def net(self, net, vat):
        return 0.0
