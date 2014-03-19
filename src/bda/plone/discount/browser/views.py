from Products.Five import BrowserView
from bda.plone.discount import message_factory as _
from yafowil.base import factory


class DiscountView(BrowserView):
    title = None
    related_forms = []
    default_form = None

    @property
    def recent_formname(self):
        return self.request.form.get('formfilter.name', self.default_form)

    def rendered_filter(self):
        form = factory(
            'form',
            name='formfilter',
            props={'action': self.request.getURL()},
        )
        form['name'] = factory(
            'label:select',
            value=self.recent_formname,
            props={
                'vocabulary': self.related_forms,
                'label': _('discount_rules', default=u'Discount Rules'),
            }
        )
        form['submit'] = factory(
            'submit',
            name='filter',
            props={
                'label': _('show', default=u'Show')
            }
        )
        return form(request=self.request)

    def rendered_form(self):
        return self.context.restrictedTraverse(self.recent_formname)()


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

