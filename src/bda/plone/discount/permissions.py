# -*- coding: utf-8 -*-
from AccessControl.Permission import addPermission

# manage discount
ManageDiscount = "bda.plone.discount: Manage Discount"
addPermission(ManageDiscount, ("Manager", "Site Administrator"))
