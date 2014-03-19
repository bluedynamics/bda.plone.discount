import json
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from yafowil.plone.form import YAMLBaseForm
from bda.plone.ajax import AjaxMessage
from bda.plone.ajax import ajax_continue
from bda.plone.ajax import ajax_form_fiddle
from bda.plone.discount import message_factory as _
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings


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
        ret = ['John', 'Sepp', 'Max']
        return self.response(ret)


class GroupsJson(JsonBase, GroupsMixin):

    def __call__(self):
        """search for group.
        """
        ret = ['Retail', 'Trade', 'Dealer', 'Master Dealer']
        return self.response(ret)


class DiscountFormBase(YAMLBaseForm):
    """Abstract discount Form.
    """
    settings_iface = None
    form_template = 'bda.plone.discount.browser:discount.yaml'
    form_name = ''
    message_factory = _
    action_resource = ''
    header_template = 'general_header.pt'
    for_label = ''
    for_required = ''
    for_callback = ''
    for_mode = 'skip'

    def form_action(self, widget, data):
        return '%s/ajaxform?form_name=%s' % \
            (self.context.absolute_url(), self.action_resource)

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

    @property
    def settings(self):
        return self.settings_iface(self.context)

    def save(self, widget, data):
        raise NotImplementedError(u'Abstract ``DiscountFormBase`` does not '
                                  u'implement ``save``')

    def next(self, request):
        message = _('changes_saved', default=u'Changes Saved')
        continuation = [
            AjaxMessage(message, 'info', None)
        ]
        ajax_continue(self.request, continuation)
        return False

    def __call__(self):
        ajax_form_fiddle(self.request, 'div.disount_form_wrapper', 'inner')
        return self.render_form()


class UserDiscountFormBase(DiscountFormBase, UsersMixin):
    header_template = 'user_header.pt'
    for_label = _('discount_form_label_user', default=u'User')
    for_required = _('discount_form_user_required',
                     default=u'User is required')
    for_callback = 'javascript:discount_form.autocomplete_user'
    for_mode = 'edit'


class GroupDiscountFormBase(DiscountFormBase, GroupsMixin):
    header_template = 'group_header.pt'
    for_label = _('discount_form_label_group', default=u'Group')
    for_required = _('discount_form_group_required',
                     default=u'Group is required')
    for_callback = 'javascript:discount_form.autocomplete_group'
    for_mode = 'edit'


class CartItemDiscountForm(DiscountFormBase):
    settings_iface = ICartItemDiscountSettings
    action_resource = 'cart_item_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass


class UserCartItemDiscountForm(UserDiscountFormBase, CartItemDiscountForm):
    settings_iface = IUserCartItemDiscountSettings
    action_resource = 'user_cart_item_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass


class GroupCartItemDiscountForm(GroupDiscountFormBase, CartItemDiscountForm):
    settings_iface = IGroupCartItemDiscountSettings
    action_resource = 'group_cart_item_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass


class CartDiscountForm(DiscountFormBase):
    settings_iface = ICartDiscountSettings
    action_resource = 'cart_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass


class UserCartDiscountForm(UserDiscountFormBase, CartDiscountForm):
    settings_iface = IUserCartDiscountSettings
    action_resource = 'user_cart_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass


class GroupCartDiscountForm(GroupDiscountFormBase, CartDiscountForm):
    settings_iface = IGroupCartDiscountSettings
    action_resource = 'group_cart_discount_form'

    @property
    def discount_value(self):
        return []

    def save(self, widget, data):
        pass
