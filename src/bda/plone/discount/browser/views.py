from Products.Five import BrowserView
from bda.plone.discount import message_factory as _
from yafowil.base import factory
from zope.component.interfaces import ISite


class DiscountView(BrowserView):
    title = None
    related_forms = []
    default_form = None

    def disable_border(self):
        if ISite.providedBy(self.context):
            self.request.set('disable_border', True)

    def rendered_filter(self):
        selection = factory(
            'label:select',
            name='discount_form_filter',
            value=self.default_form,
            props={
                'vocabulary': self.related_forms,
                'label': _('discount_rules', default=u'Discount Rules'),
            }
        )
        return selection(request=self.request)

    def rendered_form(self):
        return self.context.restrictedTraverse(self.default_form)()


class ItemDiscountView(DiscountView):
    title = _('cart_item_discount_title', default=u'Discount for Cart Items')
    default_form = 'cart_item_discount_form'
    related_forms = [
        ('cart_item_discount_form',
         _('cart_item_discount_form',
           default=u'General Rules for Cart Items')),
        ('user_cart_item_discount_form',
         _('user_cart_item_discount_form',
           default=u'User Rules for Cart Items')),
        ('group_cart_item_discount_form',
         _('group_cart_item_discount_form',
           default=u'Group Rules for Cart Items')),
    ]


class CartDiscountView(DiscountView):
    title = _('cart_discount_title', default=u'Discount for Cart')
    default_form = 'cart_discount_form'
    related_forms = [
        ('cart_discount_form',
         _('cart_discount_form',
           default=u'General Rules for Cart')),
        ('user_cart_discount_form',
         _('user_cart_discount_form',
           default=u'User Rules for Cart')),
        ('group_cart_discount_form',
         _('group_cart_discount_form',
           default=u'Group Rules for Cart')),
    ]

