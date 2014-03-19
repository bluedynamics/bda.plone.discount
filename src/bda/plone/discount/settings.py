import uuid
import plone.api
from datetime import datetime
from zope.interface import implementer
from zope.component import adapter
from node.utils import UNSET
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.uuid.interfaces import IUUID
from bda.plone.discount.interfaces import IDiscountEnabled
from bda.plone.discount.interfaces import IDiscountSettings
from bda.plone.discount.interfaces import ICartItemDiscountSettings
from bda.plone.discount.interfaces import IUserCartItemDiscountSettings
from bda.plone.discount.interfaces import IGroupCartItemDiscountSettings
from bda.plone.discount.interfaces import ICartDiscountSettings
from bda.plone.discount.interfaces import IUserCartDiscountSettings
from bda.plone.discount.interfaces import IGroupCartDiscountSettings
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.query import Any
from repoze.catalog.query import Eq
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from souper.soup import Record
from souper.soup import get_soup


FLOOR_DATETIME = datetime(1970, 1, 1, 0, 0, 0)
CEILING_DATETIME = datetime(2100, 1, 1, 0, 0, 0)


@implementer(ICatalogFactory)
class DiscountRulesCatalogFactory(object):

    def __call__(self, context=None):
        catalog = Catalog()
        # unique id of rule
        uid_indexer = NodeAttributeIndexer('uid')
        catalog[u'uid'] = CatalogFieldIndex(uid_indexer)
        # uid of context rule refers to
        context_uid_indexer = NodeAttributeIndexer('context_uid')
        catalog[u'context_uid'] = CatalogFieldIndex(context_uid_indexer)
        # rule creator user id
        creator_indexer = NodeAttributeIndexer('creator')
        catalog[u'creator'] = CatalogFieldIndex(creator_indexer)
        # rule creation date
        created_indexer = NodeAttributeIndexer('created')
        catalog[u'created'] = CatalogFieldIndex(created_indexer)
        # rule category
        category_indexer = NodeAttributeIndexer('category')
        catalog[u'category'] = CatalogFieldIndex(category_indexer)
        # rule calculation kind
        kind_indexer = NodeAttributeIndexer('kind')
        catalog[u'kind'] = CatalogFieldIndex(kind_indexer)
        # block parent rules
        block_indexer = NodeAttributeIndexer('block')
        catalog[u'block'] = CatalogFieldIndex(block_indexer)
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


@implementer(IDiscountSettings)
class PersistendDiscountSettings(object):
    soup_name = 'bda_plone_discount_rules'
    category = UNSET

    def __init__(self, context):
        self.context = context

    @property
    def rules(self):
        return get_soup(self.soup_name, self.context)

    def add_rule(self, context, kind, block, valid_from,
                 valid_to, user=UNSET, group=UNSET):
        rule = Record()
        rule.attrs['uid'] = uuid.uuid4()
        if self.category is not UNSET:
            assert(isinstance(self.category, self.unicode))
        rule.attrs['category'] = self.category
        rule.attrs['context_uid'] = uuid.UUID(IUUID(context))
        rule.attrs['creator'] = plone.api.user.get_current().getId()
        rule.attrs['created'] = datetime.datetime.now()
        assert(isinstance(kind, str))
        rule.attrs['kind'] = kind
        assert(isinstance(block, bool))
        rule.attrs['block'] = block
        if valid_from is not UNSET:
            assert(isinstance(valid_from, datetime))
        else:
            valid_from = FLOOR_DATETIME
        rule.attrs['valid_from'] = valid_from
        if valid_to is not UNSET:
            assert(isinstance(valid_to, datetime))
        else:
            valid_to = CEILING_DATETIME
        rule.attrs['valid_to'] = valid_to
        if user is not UNSET:
            assert(isinstance(user, unicode))
        rule.attrs['user'] = user
        if group is not UNSET:
            assert(isinstance(group, unicode))
        rule.attrs['group'] = group
        self.rules.add(rule)


@implementer(ICartItemDiscountSettings)
class CartItemDiscountSettings(PersistendDiscountSettings):
    category = 'cart_item'


@implementer(IUserCartItemDiscountSettings)
class UserCartItemDiscountSettings(CartItemDiscountSettings):
    pass


@implementer(IGroupCartItemDiscountSettings)
class GroupCartItemDiscountSettings(CartItemDiscountSettings):
    pass


@implementer(ICartDiscountSettings)
@adapter(IPloneSiteRoot)
class CartDiscountSettings(PersistendDiscountSettings):
    category = 'cart'


@implementer(IUserCartDiscountSettings)
@adapter(IPloneSiteRoot)
class UserCartDiscountSettings(CartDiscountSettings):
    pass


@implementer(IGroupCartDiscountSettings)
@adapter(IPloneSiteRoot)
class GroupCartDiscountSettings(CartDiscountSettings):
    pass
