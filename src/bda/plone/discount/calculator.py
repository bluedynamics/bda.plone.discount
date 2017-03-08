# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from bda.plone.cart import get_item_data_provider
from bda.plone.cart.interfaces import ICartDiscount
from bda.plone.cart.interfaces import ICartItem
from bda.plone.cart.interfaces import ICartItemDiscount
from bda.plone.discount.interfaces import ALL_PORTAL_TYPES
from bda.plone.discount.interfaces import FOR_GROUP
from bda.plone.discount.interfaces import FOR_USER
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import KIND_ABSOLUTE
from bda.plone.discount.interfaces import KIND_OFF
from bda.plone.discount.interfaces import KIND_PERCENT
from bda.plone.discount.interfaces import THRESHOLD_ITEM_COUNT
from bda.plone.discount.interfaces import THRESHOLD_PRICE
from datetime import datetime
from decimal import Decimal
from plone import api
from plone.api.exc import UserNotFoundError
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import queryAdapter
from zope.component.interfaces import ISite
from zope.interface import implementer
from zope.interface import Interface


def value_from_rule(rule, key, fallback):
    """Utility for B/C rules not providing key on rule.
    """
    val = rule.attrs.get(key)
    if not val:
        return fallback
    return val


def portal_type_from_rule(rule):
    """Utility for B/C rules providing no portal_type on rule.
    """
    return value_from_rule(rule, 'portal_type', ALL_PORTAL_TYPES)


def threshold_calculation_from_rule(rule):
    """Utility for B/C rules providing no threshold_calculation on rule.
    """
    return value_from_rule(rule, 'threshold_calculation', THRESHOLD_PRICE)


class RuleLookup(object):
    """Object for looking up discount rules on given context.
    """

    settings_iface = None
    """``IDiscountSettings`` deriving adapter interface.
    """

    for_attribute = None
    """Optional principal binding. can be ``FOR_USER`` or  ``FOR_GROUP``
    """

    def __init__(self, context, date, for_value=None):
        """Create rule lookup for context.

        :param date: Optional anchor date for matching rule effective and
        expiration date.
        :param for_value: Optional principal rules must match.
        ``RuleLookup.for_attribute`` defines whether principal name corresponds
        to a user or a group.
        """
        self.context = context
        self.date = date
        self.for_value = for_value

    @property
    def settings(self):
        """Lookup concrete settings implementation by
        ``RuleLookup.settings_iface``.
        """
        return queryAdapter(self.context, self.settings_iface)

    @property
    def rules(self):
        """Lookup all context related discount rules filtered by anchor date
        and principal.
        """
        settings = self.settings
        if settings:
            kw = dict()
            if self.for_value:
                kw[self.for_attribute] = self.for_value
            return settings.rules(self.context, date=self.date, **kw)
        return []

    def lookup(self, portal_type=None):
        """Lookup recent discount rule to apply for context.

        If no portal type given, return first rule bound to all portal types.

        If portal type given, return first portal type bound rule found,
        otherwise return first rule bound to all portal types.
        """
        # rules maching all portal types
        general = list()
        # specific portal type bound rules
        type_bound = list()
        # collect rules
        for rule in self.rules:
            if portal_type_from_rule(rule) == ALL_PORTAL_TYPES:
                general.append(rule)
            else:
                type_bound.append(rule)
        # search for rule matching given portal type and return first matching
        if portal_type:
            for rule in type_bound:
                if portal_type_from_rule(rule) == portal_type:
                    return rule
        # return first general rule
        for rule in general:
            return rule


class ItemRulesLookup(RuleLookup):
    """General item discount rule lookup.
    """
    settings_iface = ICartItemDiscountSettings


class UserItemRulesLookup(RuleLookup):
    """User bound item discount rule lookup.
    """
    settings_iface = IUserCartItemDiscountSettings
    for_attribute = FOR_USER


class GroupItemRulesLookup(RuleLookup):
    """Group bound item discount rule lookup.
    """
    settings_iface = IGroupCartItemDiscountSettings
    for_attribute = FOR_GROUP


class CartRulesLookup(RuleLookup):
    """General overall cart discount rule lookup.
    """
    settings_iface = ICartDiscountSettings


class UserCartRulesLookup(RuleLookup):
    """User bound overall cart discount rule lookup.
    """
    settings_iface = IUserCartDiscountSettings
    for_attribute = FOR_USER


class GroupCartRulesLookup(RuleLookup):
    """Group bound overall cart discount rule lookup.
    """
    settings_iface = IGroupCartDiscountSettings
    for_attribute = FOR_GROUP


class RuleAcquierer(object):
    """Object to acquire discount rules to apply for discount calculation.
    """

    lookup_factory = None
    """General discount rule related factory creating a ``RuleLookup`` deriving
    object.
    """

    user_lookup_factory = None
    """User bound discount rule related factory creating a ``RuleLookup``
    deriving object.
    """

    group_lookup_factory = None
    """Group bound discount rule related factory creating a ``RuleLookup``
    deriving object.
    """

    def __init__(self, context):
        """Create rule acquierer for given context.
        """
        # context to acquire rules from
        self.context = context
        # rule anchor date
        self.date = datetime.now()
        # get current authenticated member
        self.member = api.user.get_current()
        # set user name and user groups if authenticated member found
        self.user = None
        self.groups = None
        if self.member:
            self.user = self.member.getId()
            try:
                groups = api.group.get_groups(username=self.user)
                self.groups = [group.getId() for group in groups]
            except UserNotFoundError:
                self.groups = []

    def lookup_chain(self, context):
        """Return list of ``RuleLookup`` objects to search for discount rules.

        Lookup chain priority:

            1: User related rule lookup
            2: Group related rule lookup
            3: General rule lookup
        """
        lookups = list()
        if self.user:
            lookups.append(self.user_lookup_factory(
                context=context,
                date=self.date,
                for_value=self.user
            ))
        for group in self.groups:
            lookups.append(self.group_lookup_factory(
                context=context,
                date=self.date,
                for_value=group
            ))
        lookups.append(self.lookup_factory(context=context, date=self.date))
        return lookups

    def rules(self, portal_type=None):
        """Return rules to apply, most outer first.

        Aggregate rules through hierarchy until Plone root is reached.

        Container objects get ignored if ``IDiscountSettingsEnabled`` not
        provided.

        For each context only the first found rule from lookup chain is
        considered.

        Stops hierarchical lookup if found rule for context sets it's ``block``
        flag.
        """
        rules = list()
        context = self.context
        # traverse down at most until plone root
        while True:
            # ignore context if no discount settings enabled or no site
            if not (IDiscountSettingsEnabled.providedBy(context)
                    or ISite.providedBy(context)):
                context = aq_parent(aq_inner(context))
                continue
            rule = None
            # iterate lookup chain, break on first rule found
            for lookup in self.lookup_chain(context):
                rule = lookup.lookup(portal_type=portal_type)
                if rule:
                    break
            # add rule if found
            if rule:
                rules.append(rule)
                # break aggregating if defined
                if rule.attrs['block']:
                    break
            # plone root reached
            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))
        # aggregated rules are applied most outer first
        return reversed(rules)


class CartItemRuleAcquirer(RuleAcquierer):
    """Object to acquire cart item discount rules.
    """
    lookup_factory = ItemRulesLookup
    user_lookup_factory = UserItemRulesLookup
    group_lookup_factory = GroupItemRulesLookup


class CartRuleAcquirer(RuleAcquierer):
    """Object to acquire overall cart discount rules.
    """
    lookup_factory = CartRulesLookup
    user_lookup_factory = UserCartRulesLookup
    group_lookup_factory = GroupCartRulesLookup


class DiscountBase(object):
    """Object for calculating discount.
    """

    aquirer_factory = None
    """Factory for creating ``RuleAcquierer`` deriving object.
    """

    def __init__(self, context):
        """Create discount object for context.
        """
        self.context = context

    @property
    def acquirer(self):
        """Return concrete ``RuleAcquierer`` implementation instance.
        """
        return self.aquirer_factory(self.context)

    def apply_rule(self, value, rule, count=Decimal(1), portal_type=None):
        """Return discounted value from given value by rule for one item.

        Count is used for threshold calculation. If threshold is calculated
        from price and threshold is lower or equal value * count, value
        is returned unchanged. If threshold is calculated from item count and
        threshold is lower or equal count, value is retured unchanged.

        If portal type is given, rule applies only if matches to given or all
        portal types.
        """
        # check portal type if given
        if portal_type is not None:
            # lookup portal type on rule
            rule_pt = portal_type_from_rule(rule)
            # return value as is if rule portal type not matches given one
            if rule_pt != ALL_PORTAL_TYPES and rule_pt != portal_type:
                return value
        # check discount application threshold
        threshold = rule.attrs['threshold']
        if threshold:
            threshold = Decimal(threshold)
            # lookup threshold calculation on rule
            calculation = threshold_calculation_from_rule(rule)
            # threshold triggers on price
            if calculation == THRESHOLD_PRICE and threshold > value * count:
                return value
            # threshold triggers on item count
            if calculation == THRESHOLD_ITEM_COUNT and threshold > count:
                return value
        # get discount rule value
        rule_value = Decimal(rule.attrs['value'])
        # calculate in percent
        if rule.attrs['kind'] == KIND_PERCENT:
            value -= value / Decimal(100) * rule_value
        # calculate decrement
        if rule.attrs['kind'] == KIND_OFF:
            value -= rule_value
        # rule defines absolute value
        if rule.attrs['kind'] == KIND_ABSOLUTE:
            value = rule_value
        # value never < 0
        if value < Decimal(0):
            value = Decimal(0)
        # return discounted value
        return value

    def apply_rules(self, value, count=Decimal(1), portal_type=None):
        """Apply all rules from rule acquirer on given value. Optional count
        and portal type is considered.
        """
        rules = self.acquirer.rules(portal_type=portal_type)
        for rule in rules:
            value = self.apply_rule(
                value=value,
                rule=rule,
                count=count,
                portal_type=portal_type
            )
        # value never < 0
        if value < Decimal(0):
            value = Decimal(0)
        return value


# XXX
# DISCOUNT_FROM_GROSS = False


@implementer(ICartItemDiscount)
@adapter(ICartItem)
class CartItemDiscount(DiscountBase):
    """Discount calculator for cart items.
    """
    aquirer_factory = CartItemRuleAcquirer

    def net(self, net, vat, count):
        # net discount for one item.
        # XXX: from gross
        net = Decimal(net)
        item_discount = net - self.apply_rules(
            value=net,
            count=count,
            portal_type=self.context.portal_type
        )
        return item_discount


@implementer(ICartDiscount)
@adapter(Interface)
class CartDiscount(DiscountBase):
    """Discount calculator for overall cart.
    """
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
        cart_discount = net - self.apply_rules(value=net)
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
        cart_discount = base_net - self.apply_rules(value=base_net)
        # cart net after discount calculation
        cart_net = base_net - cart_discount
        # calculate aliquot net percent for each item in cart and calculate
        # item vat portion from discounted cart net
        aliquot_vat = Decimal(0)
        for item_net, item_vat in discounted_items:
            # avoid division / 0 if price is 0
            if not item_net:
                continue
            aliquot_net_percent = item_net * Decimal(100) / base_net
            aliquot_net = cart_net / Decimal(100) * aliquot_net_percent
            aliquot_vat += aliquot_net / Decimal(100) * item_vat
        # calculate vat difference
        vat_diff = base_vat - aliquot_vat
        return vat_diff
