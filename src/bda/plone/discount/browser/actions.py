# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from zope.component.interfaces import ISite
from zope.i18nmessageid import MessageFactory
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.interface import noLongerProvides


_ = MessageFactory('bda.plone.discount')


class EnableDisableDiscountAction(BrowserView):

    def enable_discount(self):
        directlyProvides(self.context, IDiscountSettingsEnabled)
        self.context.portal_catalog.reindexObject(
            self.context, idxs=['object_provides'], update_metadata=1)
        self.context.plone_utils.addPortalMessage(
            _(u'enabled_discount', default=u'Enabled discount on context.'))
        self.request.response.redirect(self.context.absolute_url())

    def disable_discount(self):
        noLongerProvides(self.context, IDiscountSettingsEnabled)
        self.context.portal_catalog.reindexObject(
            self.context, idxs=['object_provides'], update_metadata=1)
        self.context.plone_utils.addPortalMessage(
            _(u'disabled_discount', default=u'Disabled discount on context.'))
        self.request.response.redirect(self.context.absolute_url())

    def can_enable_discount(self):
        return not ISite.providedBy(self.context) \
            and not IDiscountSettingsEnabled.providedBy(self.context)

    def can_disable_discount(self):
        return IDiscountSettingsEnabled in directlyProvidedBy(self.context)
