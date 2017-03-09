# -*- coding: utf-8 -*-
from bda.plone.discount.interfaces import CATEGORY_CART
from bda.plone.discount.interfaces import CATEGORY_CART_ITEM
from bda.plone.discount.interfaces import CEILING_DATETIME
from bda.plone.discount.interfaces import FLOOR_DATETIME
from bda.plone.discount.interfaces import FOR_GROUP
from bda.plone.discount.interfaces import FOR_USER
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from datetime import datetime
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces import IPloneSiteRoot
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.query import Eq
from repoze.catalog.query import Ge
from repoze.catalog.query import Le
from repoze.catalog.query import NotEq
from souper.interfaces import ICatalogFactory
from souper.soup import get_soup
from souper.soup import NodeAttributeIndexer
from souper.soup import Record
from zope.component import adapter
from zope.interface import implementer

import plone.api
import uuid


@implementer(ICatalogFactory)
class DiscountRulesCatalogFactory(object):

    def __call__(self, context=None):
        catalog = Catalog()
        # uid of context rule refers to
        context_uid_indexer = NodeAttributeIndexer('context_uid')
        catalog[u'context_uid'] = CatalogFieldIndex(context_uid_indexer)
        # rule category
        category_indexer = NodeAttributeIndexer('category')
        catalog[u'category'] = CatalogFieldIndex(category_indexer)
        # rule valid from date
        valid_from_indexer = NodeAttributeIndexer('valid_from')
        catalog[u'valid_from'] = CatalogFieldIndex(valid_from_indexer)
        # rule valid to date
        valid_to_indexer = NodeAttributeIndexer('valid_to')
        catalog[u'valid_to'] = CatalogFieldIndex(valid_to_indexer)
        # user this rule applies
        user_indexer = NodeAttributeIndexer('user')
        catalog[u'user'] = CatalogFieldIndex(user_indexer)
        # group this rule applies
        group_indexer = NodeAttributeIndexer('group')
        catalog[u'group'] = CatalogFieldIndex(group_indexer)
        return catalog


def create_rule(uid, category, creator, index, kind, block, value, threshold,
                threshold_calculation, portal_type, valid_from, valid_to,
                user='', group=''):
    rule = Record()
    rule.attrs['index'] = index
    assert(isinstance(category, str))
    rule.attrs['category'] = category
    rule.attrs['context_uid'] = uid
    rule.attrs['creator'] = creator
    rule.attrs['created'] = datetime.now()
    assert(isinstance(kind, str))
    rule.attrs['kind'] = kind
    assert(isinstance(block, bool))
    rule.attrs['block'] = block
    assert(isinstance(value, float))
    rule.attrs['value'] = value
    if threshold:
        assert(isinstance(threshold, float))
    rule.attrs['threshold'] = threshold
    rule.attrs['threshold_calculation'] = threshold_calculation
    rule.attrs['portal_type'] = portal_type
    if valid_from:
        assert(isinstance(valid_from, datetime))
    else:
        valid_from = FLOOR_DATETIME
    rule.attrs['valid_from'] = valid_from
    if valid_to:
        assert(isinstance(valid_to, datetime))
    else:
        valid_to = CEILING_DATETIME
    rule.attrs['valid_to'] = valid_to
    assert(isinstance(user, str))
    rule.attrs['user'] = user
    assert(isinstance(group, str))
    rule.attrs['group'] = group
    return rule


@implementer(IDiscountSettings)
class PersistendDiscountSettings(object):
    soup_name = 'bda_plone_discount_rules'
    category = ''
    for_attribute = None

    def __init__(self, context):
        self.context = context

    @property
    def rules_soup(self):
        return get_soup(self.soup_name, self.context)

    def rules(self, context, date=None, user='', group=''):
        context_uid = uuid.UUID(IUUID(context))
        query = Eq('context_uid', context_uid) & Eq('category', self.category)
        if date is not None:
            query = query & Le('valid_from', date) & Ge('valid_to', date)
        if self.for_attribute == FOR_USER:
            if group:
                msg = u'``group`` keyword must not be given if scope is user'
                raise ValueError(msg)
            if user:
                query = query & Eq('user', user)
            else:
                query = query & NotEq('user', '')
        elif self.for_attribute == FOR_GROUP:
            if user:
                msg = u'``user`` keyword must not be given if scope is group'
                raise ValueError(msg)
            if group:
                query = query & Eq('group', group)
            else:
                query = query & NotEq('group', '')
        else:
            if user or group:
                msg = u'``user`` and ``group`` keywords must not be given ' +\
                      u'if scope is general'
                raise ValueError(msg)
            query = query & Eq('user', '') & Eq('group', '')
        return self.rules_soup.query(query,
                                     sort_index='valid_from',
                                     reverse=True)

    def delete_rules(self, rules):
        soup = self.rules_soup
        for rule in [_ for _ in rules]:
            del soup[rule]

    def add_rule(self, context, index, kind, block, value, threshold,
                 threshold_calculation, portal_type, valid_from, valid_to,
                 user='', group=''):
        rule = create_rule(
            uid=uuid.UUID(IUUID(context)),
            category=self.category,
            creator=plone.api.user.get_current().getId(),
            index=index,
            kind=kind,
            block=block,
            value=value,
            threshold=threshold,
            threshold_calculation=threshold_calculation,
            portal_type=portal_type,
            valid_from=valid_from,
            valid_to=valid_to,
            user=user,
            group=group)
        self.rules_soup.add(rule)


@implementer(ICartItemDiscountSettings)
class CartItemDiscountSettings(PersistendDiscountSettings):
    category = CATEGORY_CART_ITEM


@implementer(IUserCartItemDiscountSettings)
class UserCartItemDiscountSettings(CartItemDiscountSettings):
    for_attribute = FOR_USER


@implementer(IGroupCartItemDiscountSettings)
class GroupCartItemDiscountSettings(CartItemDiscountSettings):
    for_attribute = FOR_GROUP


@implementer(ICartDiscountSettings)
@adapter(IPloneSiteRoot)
class CartDiscountSettings(PersistendDiscountSettings):
    category = CATEGORY_CART


@implementer(IUserCartDiscountSettings)
@adapter(IPloneSiteRoot)
class UserCartDiscountSettings(CartDiscountSettings):
    for_attribute = FOR_USER


@implementer(IGroupCartDiscountSettings)
@adapter(IPloneSiteRoot)
class GroupCartDiscountSettings(CartDiscountSettings):
    for_attribute = FOR_GROUP
