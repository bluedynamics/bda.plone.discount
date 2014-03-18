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


class DiscountFormBase(YamlForm):
    """Abstract discount Form.
    """
    form_template = 'bda.plone.discount.browser:discount.yaml'
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
            _('percent', _('percent', default=u'Percent')),
            _('off', _('off', default=u'Off')),
            _('absolute', _('absolute', default=u'Absolute')),
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


class ItemDiscountForm(DiscountFormBase):
    action_resource = '@@item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class UserItemDiscountForm(UserDiscountFormBase, ItemDiscountForm):
    action_resource = '@@user_item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class GroupItemDiscountForm(GroupDiscountFormBase, ItemDiscountForm):
    action_resource = '@@group_item_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class OverallDiscountForm(DiscountFormBase):
    action_resource = '@@overall_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class UserOverallDiscountForm(UserDiscountFormBase, OverallDiscountForm):
    action_resource = '@@user_overall_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass


class GroupOverallDiscountForm(GroupDiscountFormBase, OverallDiscountForm):
    action_resource = '@@group_overall_discount_form'

    @property
    def discount_value(self):
        pass

    def save(self, widget, data):
        pass

    def next(self):
        pass
