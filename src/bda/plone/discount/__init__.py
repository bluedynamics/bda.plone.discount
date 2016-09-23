# -*- coding: utf-8 -*-
from bda.plone.discount import permissions  # noqa
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer


message_factory = MessageFactory('bda.plone.discount')


# static uuid for the PortalRoot, as it doesn't have a uuid by default
UUID_PLONE_ROOT = '77c4390d-1179-44ba-9d57-46d23ac292c6'


@implementer(IUUID)
@adapter(IPloneSiteRoot)
def plone_root_uuid(context):
    """Adapter, which returns the static UUID for the IPloneSiteRoot, so that
    this uuid can be used to be indexed in our souper storage.
    """
    return UUID_PLONE_ROOT
