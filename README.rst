bda.plone.discount
==================


Restrictions with souper.plone
------------------------------

- Make sure you do not move discount rules soup away from portal root. This
  will end up in unexpected behavior and errors.


Requirements
------------

Discounting information for content items:

- Define price absolute (in currency) or relative to the canonical one (in %)
- Define a price for a user
- Define a price for a group
- Define these prices for a specific date range (expiration date would not work
  here, should be defined for each price)

Following cascading rules apply:

- Base price is the canonical one (set in shop tab on buyable item)
- Special price overrules canonical one (if set relative [in %], it gets
  calculated from canonical price)
- If more than one general special price found (i.e if validity period
  overlaps), first one found applies
- Special prices defined for groups overrule a generic special price
- Special prices defined for users overrule a generic special price and special
  prices defined for groups
- Maybe we want to handle special prices accumulated if relative to the
  canonical price (i.e. special customer gets 8 % discount)

The UI implementation should be as follows:

- The buyable item gets an additional tab "pricing"
- The pricing view contains 3 form arrays
  (http://demo.yafowil.info/++widget++yafowil.widget.array/index.html), one for
  generic pricing, one for group pricing and one for user pricing
- These array entries look like:
  [relative/absolute (selection)][value][valid from (date)][valid to (date)]
  [user/group (for array 2 and 3)][+][-]
- User/group field gets an autocomplete field
  (http://demo.yafowil.info/++widget++yafowil.widget.autocomplete/index.html)
- Valid from and valid to gets a datetime field
  (http://demo.yafowil.info/++widget++yafowil.widget.datetime/index.html)

Global Discount:

- 10% off when above EUR 200
- 20% off when above EUR 500
- EUR 20 off when above a certain limit.
- Coupon Codes/Vouchers
