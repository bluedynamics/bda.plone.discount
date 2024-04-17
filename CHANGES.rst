
Changelog
=========

2.0b1 (2024-04-17)
------------------

- No longer support for z3c.autoinclude.
  [jensens]

- Adopt import to latest cart changes.
  [jensens]

- Code style black. isort imports.
  [jensens]

- Python 2/3 compatibility
  [agitator]

- Update version and classifiers - 2.x targets Plone 5.1/5.2 without Archetypes
  [agitator]

- Update resource loading for discount view
  [agitator]

1.0a1 (unreleased)
------------------

- Replace unittest2 with untittest
  [agitator]

- Item discount threshold can be defined either by price or item count.
  [rnix]

- Add portal type filter support for cart item discount rules.
  [rnix]

- Ignore all non ``IDiscountSettingsEnabled`` and non ``ISite`` providing
  contexts in ``RuleAcquierer.rules``.
  [rnix]

- Bind all views to ``IDiscountExtensionLayer``.
  [rnix]

- Make ``discount_form`` global in ``discount.js`` in order to make discount
  form switch work again.
  [rnix]

- Add actions to enable and disable item discount
  (``IDiscountSettingsEnabled``) on context.
  [rnix]

- Plone 5 update.
  [agitator]


0.3
---

- JSHint JavaScript.
  [thet]


0.2
---

- Translate ``changes_saved`` ajax message directly in view class.
  [rnix]

- Add ``user`` and ``group`` keyword arguments to
  ``bda.plone.discount.settings.PersistendDiscountSettings.rules`` function.
  Restrict the use of these keywords by defined ``for_attribute`` scope.
  [rnix]

- Avoid division / 0 in ``bda.plone.discount.calculator.CartDiscount.vat``
  [rnix]

- Only hide border for global dicsount_views.
  [rnix]


0.1
---

- initial work
  [rnix]
