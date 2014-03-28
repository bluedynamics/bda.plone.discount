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
        # XXX: return value as list of neighbor rules
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
                groups = api.group.get_groups(username=self.member)
                self.groups = [group.getId() for group in groups]
            except UserNotFoundError:
                self.groups = []

    def lookup_cascade(self, context):
        lookups = list()
        if self.user:
            user_lookup = self.user_lookup_factory(
                context, self.date, self.user)
            lookups.append(user_lookup)
        for group in self.groups:
            group_lookup = self.group_lookup_factory(
                context, self.date, group)
            lookups.append(group_lookup)
        lookups.append(self.lookup_factory(context, self.date))
        return lookups

    @property
    def rules(self):
        # return rules to apply, most outer first
        rules = list()
        context = self.context
        while True:
            rule = None
            for lookup in self.lookup_cascade(context):
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

    def apply_rule(self, value, rule, count=Decimal(1)):
        # return value after rule applied
        # if threshold not reached return unchanged value
        # count is needed for rule types KIND_OFF and KIND_ABSOLUTE
        # anyway value needs to be the undiscounted total for this item
        # in order for correct threshold consideration.
        threshold = rule.attrs['threshold']
        if threshold and Decimal(threshold) > value:
            return value
        rule_value = Decimal(rule.attrs['value'])
        # calculate in percent
        if rule.attrs['kind'] == KIND_PERCENT:
            value -= value / Decimal(100) * rule_value
        # calculate decrement
        if rule.attrs['kind'] == KIND_OFF:
            value -= rule_value * count
        # rule defines absolute value
        if rule.attrs['kind'] == KIND_ABSOLUTE:
            value = rule_value * count
        # value never < 0
        if value < Decimal(0):
            value = Decimal(0)
        return value

    def apply_rules(self, value, count=Decimal(1)):
        rules = self.acquirer.rules
        for rule in rules:
            value = self.apply_rule(value, rule, count=count)
        # value never < 0
        if value < Decimal(0):
            value = Decimal(0)
        return value


# XXX
DISCOUNT_FROM_GROSS = False


@implementer(ICartItemDiscount)
@adapter(ICartItem)
class CartItemDiscount(DiscountBase):
    aquirer_factory = CartItemRuleAcquirer

    def net(self, net, vat, count):
        # net discount for one item.
        # XXX: from gross
        net = Decimal(net)
        item_discount = net - self.apply_rules(net * count, count) / count
        return item_discount


@implementer(ICartDiscount)
@adapter(Interface)
class CartDiscount(DiscountBase):
    aquirer_factory = CartRuleAcquirer

    def _discounted_items(self, items):
        # return list of 2-tuples containing (net, vat percent) of discounted
        # items in cart. count is already considered.
        # XXX: from gross
        result = list()
        cat = api.portal.get_tool(name='portal_catalog')
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = get_item_data_provider(brain[0].getObject())
            discount_net = data.discount_net(count)
            item_net = Decimal(str(data.net)) - discount_net
            result.append((item_net * count, Decimal(str(data.vat))))
        return result

    def net(self, items):
        # XXX: from gross
        net = Decimal(0)
        for item_net, _ in self._discounted_items(items):
            net += item_net
        cart_discount = net - self.apply_rules(net)
        return cart_discount

    def vat(self, items):
        # XXX: from gross
        discounted_items = self._discounted_items(items)
        base_net = Decimal(0)
        base_vat = Decimal(0)
        # calculate cart base net and vat before cart discount has been applied
        for item_net, item_vat in discounted_items:
            base_net += item_net
            base_vat += item_net / Decimal(100) * item_vat
        # calculate total cart discount
        cart_discount = base_net - self.apply_rules(base_net)
        # cart net after discount calculation
        cart_net = base_net - cart_discount
        # calculate aliquot net percent for each item in cart and calculate
        # item vat portion from discounted cart net
        aliquot_vat = Decimal(0)
        for item_net, item_vat in discounted_items:
            aliquot_net_percent = item_net * Decimal(100) / base_net
            aliquot_net = cart_net / Decimal(100) * aliquot_net_percent
            aliquot_vat += aliquot_net / Decimal(100) * item_vat
        # calculate vat difference
        vat_diff = base_vat - aliquot_vat
        return vat_diff
