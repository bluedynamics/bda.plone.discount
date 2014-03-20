from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter
from bda.plone.cart.interfaces import ICartItem
from bda.plone.cart.interfaces import IDiscount
from bda.plone.cart.interfaces import ICartDiscount
from bda.plone.cart.interfaces import ICartItemDiscount
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings


@implementer(IDiscount)
class Discount(object):

    def __init__(self, context):
        self.context = context

    def aggregated_rules(self):
        pass

    def reduced_net(self, net, vat):
        print 'Discount.reduced_net'
        return net


@implementer(ICartItemDiscount)
@adapter(ICartItem)
class CartItemDiscount(Discount):
    pass


@implementer(ICartDiscount)
@adapter(Interface)
class CartDiscount(Discount):
    pass
