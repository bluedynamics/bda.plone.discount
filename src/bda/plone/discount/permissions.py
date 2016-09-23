# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles


# manage discount
ManageDiscount = 'bda.plone.discount: Manage Discount'
setDefaultRoles(ManageDiscount,
                ('Manager', 'Site Administrator'))
