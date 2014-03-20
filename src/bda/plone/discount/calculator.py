from Acquisition import aq_inner
from Acquisition import aq_parent
from bda.plone.cart.interfaces import ICartItem
from bda.plone.cart.interfaces import ICartDiscount
from bda.plone.cart.interfaces import ICartItemDiscount
from bda.plone.discount.interfaces import FOR_USER
from bda.plone.discount.interfaces import FOR_GROUP
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from datetime import datetime
from Products.CMFPlone.interface import IPloneSiteRoot
from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter
from zope.component import queryAdapter
import plone.api


class RulesLookup(object):
    settings_iface = None
    for_attribute = None

    def __init__(self, context, date, for_value=None):
        self.context = context
        self.date = date
        self.for_ = for_value

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


class ItemRulesLookup(RulesLookup):
    settings_iface = ICartItemDiscountSettings


class UserItemRulesLookup(RulesLookup):
    settings_iface = IUserCartItemDiscountSettings
    for_attribute = FOR_USER


class GroupItemRulesLookup(RulesLookup):
    settings_iface = IGroupCartItemDiscountSettings
    for_attribute = FOR_GROUP


class CartRulesLookup(RulesLookup):
    settings_iface = ICartDiscountSettings


class UserCartRulesLookup(RulesLookup):
    settings_iface = IUserCartDiscountSettings
    for_attribute = FOR_USER


class GroupCartRulesLookup(RulesLookup):
    settings_iface = IGroupCartDiscountSettings
    for_attribute = FOR_GROUP


class RuleAcquierer(object):
    lookup_factory = None
    user_lookup_factory = None
    group_lookup_factory = None

    def __init__(self, context):
        self.context = context
        self.date = datetime.now()
        self.member = plone.api.user.get_current()
        self.user = None
        self.groups = None
        if self.member:
            self.user = self.member.getId()
            self.groups = plone.api.group.get_groups(username=self.member)

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
        lookups.append(self.lookup_factory(context, self.date))
        return lookups

    def acquire(self):
        rules = list()
        context = self.context
        while True:
            rule = None
            for lookup in self.lookup_cascade:
                rule = lookup.lookup()
                if rule:
                    break
            rules.append(rule)
            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(self.context))
        return rules


class CartItemRuleAcquirer(RuleAcquierer):
    lookup_factory = ItemRulesLookup
    user_lookup_factory = UserItemRulesLookup
    group_lookup_factory = GroupItemRulesLookup


class CartRuleAcquirer(RuleAcquierer):
    lookup_factory = CartRulesLookup
    user_lookup_factory = UserCartRulesLookup
    group_lookup_factory = GroupCartRulesLookup


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
