from Acquisition import aq_inner
from Acquisition import aq_parent
from bda.plone.cart import get_item_data_provider
from bda.plone.cart.interfaces import ICartItem
from bda.plone.cart.interfaces import ICartDiscount
from bda.plone.cart.interfaces import ICartItemDiscount
from bda.plone.discount.interfaces import FOR_USER
from bda.plone.discount.interfaces import FOR_GROUP
from bda.plone.discount.interfaces import KIND_PERCENT
from bda.plone.discount.interfaces import KIND_OFF
from bda.plone.discount.interfaces import KIND_ABSOLUTE
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from datetime import datetime
from decimal import Decimal
from plone import api
from plone.api.exc import UserNotFoundError
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter
from zope.component import queryAdapter


class RuleLookup(object):
    settings_iface = None
    for_attribute = None

    def __init__(self, context, date, for_value=None):
        self.context = context
        self.date = date
        self.for_value = for_value

    @property
    def settings(self):
        return queryAdapter(self.context, self.settings_iface)

    @property
    def rules(self):
        settings = self.settings
        if settings:
            return settings.rules(self.context, date=self.date)
        return []

    def lookup(self):
        for_value = self.for_value
        # if for_value given check against for_attribute
        if for_value:
            for rule in self.rules:
                if rule.attrs[self.for_attribute] == for_value:
                    return rule
        # no for filter
        else:
            for rule in self.rules:
                return rule


class ItemRulesLookup(RuleLookup):
    settings_iface = ICartItemDiscountSettings


class UserItemRulesLookup(RuleLookup):
    settings_iface = IUserCartItemDiscountSettings
    for_attribute = FOR_USER


class GroupItemRulesLookup(RuleLookup):
    settings_iface = IGroupCartItemDiscountSettings
    for_attribute = FOR_GROUP


class CartRulesLookup(RuleLookup):
    settings_iface = ICartDiscountSettings


class UserCartRulesLookup(RuleLookup):
    settings_iface = IUserCartDiscountSettings
    for_attribute = FOR_USER


class GroupCartRulesLookup(RuleLookup):
    settings_iface = IGroupCartDiscountSettings
    for_attribute = FOR_GROUP


class RuleAcquierer(object):
    lookup_factory = None
    user_lookup_factory = None
    group_lookup_factory = None

    def __init__(self, context):
        self.context = context
        self.date = datetime.now()
        self.member = api.user.get_current()
        self.user = None
        self.groups = None
        if self.member:
            self.user = self.member.getId()
            try:
                self.groups = api.group.get_groups(username=self.member)
            except UserNotFoundError:
                self.groups = []

    @property
    def lookup_cascade(self):
        lookups = list()
        if self.user:
            user_lookup = self.user_lookup_factory(
                self.context, self.date, self.user)
            lookups.append(user_lookup)
        for group in self.groups:
            group_lookup = self.group_lookup_factory(
                self.context, self.date, group)
            lookups.append(group_lookup)
        lookups.append(self.lookup_factory(self.context, self.date))
        return lookups

    @property
    def rules(self):
        # return rules to apply, most outer first
        rules = list()
        context = self.context
        while True:
            rule = None
            for lookup in self.lookup_cascade:
                rule = lookup.lookup()
                if rule:
                    break
            if rule:
                rules.append(rule)
                if rule.attrs['block']:
                    break
            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))
        return reversed(rules)


class CartItemRuleAcquirer(RuleAcquierer):
    lookup_factory = ItemRulesLookup
    user_lookup_factory = UserItemRulesLookup
    group_lookup_factory = GroupItemRulesLookup


class CartRuleAcquirer(RuleAcquierer):
    lookup_factory = CartRulesLookup
    user_lookup_factory = UserCartRulesLookup
    group_lookup_factory = GroupCartRulesLookup


class DiscountBase(object):
    aquirer_factory = None

    def __init__(self, context):
        self.context = context

    @property
    def acquirer(self):
        return self.aquirer_factory(self.context)

    def apply_rule(self, value, rule):
        # return value after rule applied
        # if threshold not reached return unchanged value
        if rule.attrs['threshold'] > value:
            return value
        # calculate in percent
        if rule.attrs['kind'] == KIND_PERCENT:
            value -= value / 100.0 * rule.attrs['value']
        # calculate decrement
        if rule.attrs['kind'] == KIND_OFF:
            value -= rule.attrs['value']
        # rule defines absolute value
        if rule.attrs['kind'] == KIND_ABSOLUTE:
            value = rule.attrs['value']
        # price should never be < 0
        if value < 0:
            return 0.0
        return value

    def apply_rules(self, value):
        rules = self.acquirer.rules
        for rule in rules:
            value -= value - self.apply_rule(value, rule)
        return value


@implementer(ICartItemDiscount)
@adapter(ICartItem)
class CartItemDiscount(DiscountBase):
    aquirer_factory = CartItemRuleAcquirer

    def net(self, net, vat, count):
        return Decimal(0)
        # XXX: from gross
        #return net - self.apply_rules(net)


@implementer(ICartDiscount)
@adapter(Interface)
class CartDiscount(DiscountBase):
    aquirer_factory = CartRuleAcquirer

    def net(self, items):
        return Decimal(0)
        # XXX: from gross
        #net = 0.0
        #cat = api.portal.get_tool(name='portal_catalog')
        #for uid, count, comment in items:
        #    brain = cat(UID=uid)
        #    if not brain:
        #        continue
        #    data = get_item_data_provider(brain[0].getObject())
        #    net += data.net - data.discount_net * float(count)
        #return self.apply_rules(net)

    def vat(self, items):
        return Decimal(0)
        # XXX: from gross
        #vat = 0.0
        #cat = api.portal.get_tool(name='portal_catalog')
        #for uid, count, comment in items:
        #    brain = cat(UID=uid)
        #    if not brain:
        #        continue
        #    data = get_item_data_provider(brain[0].getObject())
        #    net = self.apply_rules(data.net - data.discount_net)
        #    vat += (net / 100.0 * data.vat) * float(count)
        #return vat
