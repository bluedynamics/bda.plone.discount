# -*- coding: utf-8 -*-
from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.ajax import AjaxMessage
from bda.plone.ajax import ajax_continue
from bda.plone.ajax import ajax_form_fiddle
from bda.plone.discount import message_factory as _
from bda.plone.discount.interfaces import ALL_PORTAL_TYPES
from bda.plone.discount.interfaces import CEILING_DATETIME
from bda.plone.discount.interfaces import FLOOR_DATETIME
from bda.plone.discount.interfaces import FOR_GROUP
from bda.plone.discount.interfaces import FOR_USER
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import KIND_ABSOLUTE
from bda.plone.discount.interfaces import KIND_OFF
from bda.plone.discount.interfaces import KIND_PERCENT
from bda.plone.discount.interfaces import THRESHOLD_ITEM_COUNT
from bda.plone.discount.interfaces import THRESHOLD_PRICE
from node.utils import UNSET
from plumber import plumbing
from yafowil.plone.form import CSRFProtectionBehavior
from yafowil.plone.form import YAMLBaseForm
from zope.i18n import translate
from zope.site.hooks import getSite

import json
import plone.api


class JsonBase(BrowserView):

    def _match(self, name, filter):
        name = name.lower()
        filter = filter.lower()
        # wildcard match
        if filter.find('*') != -1:
            # everything matches
            if filter == '*':
                return True
            # wildcard match like '*foo'
            elif filter.startswith('*'):
                if name.endswith(filter[1:]):
                    return True
            # wildcard match like 'foo*'
            elif filter.endswith('*'):
                if name.startswith(filter[:-1]):
                    return True
            # wildacard match like '*foo*'
            else:
                if name.find(filter[1:-1]) != -1:
                    return True
        # exact match
        else:
            if name == filter:
                return True
        return False

    def response(self, result):
        return json.dumps(result)


class UsersJson(JsonBase):

    def __call__(self):
        ret = list()
        filter = self.request.form.get('filter')
        for user in plone.api.user.get_users():
            user_id = user.getId()
            if self._match(user_id, filter):
                ret.append(user_id)
        return self.response(ret)


class GroupsJson(JsonBase):

    def __call__(self):
        ret = list()
        filter = self.request.form.get('filter')
        for group in plone.api.group.get_groups():
            group_id = group.getId()
            if self._match(group_id, filter):
                ret.append(group_id)
        return self.response(ret)


@plumbing(CSRFProtectionBehavior)
class DiscountFormBase(YAMLBaseForm):
    """Abstract discount Form.
    """
    settings_iface = None
    form_template = 'bda.plone.discount.browser:discount.yaml'
    form_name = ''
    message_factory = _
    action_resource = ''
    header_template = 'general_header.pt'
    portal_type_mode = 'edit'
    for_attribute = UNSET
    for_label = ''
    for_required = ''
    for_callback = ''
    for_mode = 'skip'

    def form_action(self, widget, data):
        return '%s/ajaxform?form_name=%s' % \
            (self.context.absolute_url(), self.action_resource)

    def discount_item(self, rule):
        get = rule.attrs.get
        value = dict()
        value['kind'] = get('kind', UNSET)
        value['block'] = get('block', True)
        value['value'] = get('value', UNSET)
        value['threshold'] = get('threshold', UNSET)
        value['threshold_calculation'] = get('threshold_calculation', UNSET)
        value['portal_type'] = get('portal_type', UNSET)
        value['valid_from'] = UNSET
        valid_from = get('valid_from', FLOOR_DATETIME)
        if valid_from != FLOOR_DATETIME:
            value['valid_from'] = valid_from
        value['valid_to'] = UNSET
        valid_to = get('valid_to', CEILING_DATETIME)
        if valid_to != CEILING_DATETIME:
            value['valid_to'] = valid_to
        for_attr = self.for_attribute
        if for_attr:
            value['for'] = get(for_attr, UNSET)
        return value

    @property
    def settings(self):
        return self.settings_iface(self.context)

    @property
    def discount_value(self):
        values = list()
        rules = self.settings.rules(self.context)
        rules = sorted(rules, key=lambda x: x.attrs.get('index', 0))
        for rule in rules:
            values.append(self.discount_item(rule))
        return values

    @property
    def discount_header(self):
        return ViewPageTemplateFile(self.header_template)(self)

    @property
    def kind_vocabulary(self):
        return [
            (KIND_PERCENT, _('percent', default=u'Percent')),
            (KIND_OFF, _('off', default=u'Off')),
            (KIND_ABSOLUTE, _('absolute', default=u'Absolute')),
        ]

    @property
    def threshold_calculation_vocabulary(self):
        return [
            (THRESHOLD_PRICE, _('price', default=u'Price')),
            (THRESHOLD_ITEM_COUNT, _('item_count', default=u'Item Count')),
        ]

    @property
    def portal_type_vocabulary(self):
        site = getSite()
        portal_types = getToolByName(site, 'portal_types', None)
        request = aq_get(portal_types, 'REQUEST', None)
        vocab = [
            (ALL_PORTAL_TYPES, _('all', default=u'All'))
        ]
        for portal_type in portal_types.listContentTypes():
            vocab.append((
                portal_type,
                translate(portal_types[portal_type].Title(), context=request)
            ))
        return vocab

    def save(self, widget, data):
        settings = self.settings
        existing = self.settings.rules(self.context)
        settings.delete_rules(existing)
        extracted = data.fetch('discount_form.discount').extracted
        index = 0
        for rule in extracted:
            user = ''
            group = ''
            if self.for_attribute == FOR_USER:
                user = rule['for'] and rule['for'] or user
            if self.for_attribute == FOR_GROUP:
                group = rule['for'] and rule['for'] or group
            settings.add_rule(
                context=self.context,
                index=index,
                kind=rule['kind'],
                block=rule['block'],
                value=rule['value'],
                threshold=rule['threshold'],
                threshold_calculation=rule['threshold_calculation'],
                portal_type=rule.get('portal_type', UNSET),
                valid_from=rule['valid_from'],
                valid_to=rule['valid_to'],
                user=user,
                group=group)
            index += 1

    def next(self, request):
        message = translate(_('changes_saved', default=u'Changes Saved'),
                            context=self.request)
        continuation = [
            AjaxMessage(message, 'info', None)
        ]
        ajax_continue(self.request, continuation)
        return False

    def __call__(self):
        # disable diazo theming if ajax call
        if '_' in self.request.form:
            self.request.response.setHeader('X-Theme-Disabled', 'True')
        ajax_form_fiddle(self.request, 'div.disount_form_wrapper', 'inner')
        return self.render_form()


class UserDiscountFormBase(DiscountFormBase):
    header_template = 'user_header.pt'
    for_attribute = FOR_USER
    for_label = _('discount_form_label_user', default=u'User')
    for_required = _('discount_form_user_required',
                     default=u'User is required')
    for_callback = 'javascript:discount_form.autocomplete_user'
    for_mode = 'edit'


class GroupDiscountFormBase(DiscountFormBase):
    header_template = 'group_header.pt'
    for_attribute = FOR_GROUP
    for_label = _('discount_form_label_group', default=u'Group')
    for_required = _('discount_form_group_required',
                     default=u'Group is required')
    for_callback = 'javascript:discount_form.autocomplete_group'
    for_mode = 'edit'


class CartItemDiscountForm(DiscountFormBase):
    settings_iface = ICartItemDiscountSettings
    action_resource = 'cart_item_discount_form'


class UserCartItemDiscountForm(UserDiscountFormBase, CartItemDiscountForm):
    settings_iface = IUserCartItemDiscountSettings
    action_resource = 'user_cart_item_discount_form'


class GroupCartItemDiscountForm(GroupDiscountFormBase, CartItemDiscountForm):
    settings_iface = IGroupCartItemDiscountSettings
    action_resource = 'group_cart_item_discount_form'


class CartDiscountForm(DiscountFormBase):
    settings_iface = ICartDiscountSettings
    action_resource = 'cart_discount_form'
    portal_type_mode = 'skip'

    @property
    def kind_vocabulary(self):
        return [
            (KIND_PERCENT, _('percent', default=u'Percent')),
            (KIND_OFF, _('off', default=u'Off'))
        ]

    @property
    def threshold_calculation_vocabulary(self):
        return [
            (THRESHOLD_PRICE, _('price', default=u'Price'))
        ]


class UserCartDiscountForm(UserDiscountFormBase, CartDiscountForm):
    settings_iface = IUserCartDiscountSettings
    action_resource = 'user_cart_discount_form'


class GroupCartDiscountForm(GroupDiscountFormBase, CartDiscountForm):
    settings_iface = IGroupCartDiscountSettings
    action_resource = 'group_cart_discount_form'
