import json
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from yafowil.plone.form import YAMLForm
from bda.plone.discount import message_factory as _


class UsersMixin(object):
    pass


class GroupsMixin(object):
    pass


class JsonBase(BrowserView):

    def response(self, result):
        return json.dumps(result)


class UsersJson(JsonBase, UsersMixin):

    def __call__(self):
        """search for user.
        """
        ret = list()
        return self.response(ret)


class GroupsJson(JsonBase, GroupsMixin):

    def __call__(self):
        """search for group.
        """
        ret = list()
        return self.response(ret)


class DiscountFormBase(YAMLForm):
    """Abstract discount Form.
    """
    form_template = 'bda.plone.discount.browser:discount.yaml'
    form_name = ''
    message_factory = _
    action_resource = ''
    header_template = 'general_header.pt'
    for_label = ''
    for_callback = ''
    for_mode = 'skip'

    @property
    def discount_value(self):
        raise NotImplementedError(u'Abstract ``DiscountFormBase`` does not '
                                  u'implement ``discount_value``')

    @property
    def discount_header(self):
        return ViewPageTemplateFile(self.header_template)(self)

    @property
    def kind_vocabulary(self):
        return [
            ('percent', _('percent', _('percent', default=u'Percent'))),
            ('off', _('off', _('off', default=u'Off'))),
            ('absolute', _('absolute', _('absolute', default=u'Absolute'))),
        ]

    def save(self, widget, data):
        raise NotImplementedError(u'Abstract ``DiscountFormBase`` does not '
                                  u'implement ``save``')

    def next(self, request):
        raise NotImplementedError(u'Abstract ``DiscountFormBase`` does not '
                                  u'implement ``next``')


class UserDiscountFormBase(DiscountFormBase, UsersMixin):
    header_template = 'user_header.pt'
    for_label = _('discount_form_label_user', default=u'User')
    for_callback = 'javascript:discount_form.autocomplete_user'
    for_mode = 'edit'


class GroupDiscountFormBase(DiscountFormBase, GroupsMixin):
    header_template = 'group_header.pt'
    for_label = _('discount_form_label_group', default=u'Group')
    for_callback = 'javascript:discount_form.autocomplete_group'
    for_mode = 'edit'


class CartItemDiscountForm(DiscountFormBase):
    action_resource = 'cart_item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class UserCartItemDiscountForm(UserDiscountFormBase, CartItemDiscountForm):
    action_resource = 'user_cart_item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class GroupCartItemDiscountForm(GroupDiscountFormBase, CartItemDiscountForm):
    action_resource = 'group_cart_item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class CartDiscountForm(DiscountFormBase):
    action_resource = 'cart_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class UserCartDiscountForm(UserDiscountFormBase, CartDiscountForm):
    action_resource = 'user_cart_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class GroupCartDiscountForm(GroupDiscountFormBase, CartDiscountForm):
    action_resource = 'group_cart_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass
