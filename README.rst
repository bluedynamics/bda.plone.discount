bda.plone.discount
==================

This package contains forms for defining discounting rules for buyable items,
both on per item basis and for overall cart, and the corresponding calculation
adapters.


Installation
------------

This package is part of the ``bda.plone.shop`` stack. Please refer to
``https://github.com/bluedynamics/bda.plone.shop`` for installation
instructions.


Restrictions with souper.plone
------------------------------

- Make sure you do not move discount rules soup away from portal root. This
  will end up in unexpected behavior and errors.


TODO
----

- Currently discount is calculated from net prices. Make it possible to control
  whether discount should be calculated from gross prices.

- Implement Vouchers / Coupons.

- Implement "block neighbor" flag and consider neighbor rules as well as
  parental rules.


Contributors
------------

- Robert Niederreiter (Author)
- Ezra Holder
