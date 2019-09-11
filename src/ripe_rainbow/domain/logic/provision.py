#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_admin
import appier_export

from .. import parts

class ProvisionPart(parts.Part):

    def reset(self, api = None, base = None, ctx = None):
        api = api or self.export_api(base = base, ctx = ctx)
        api.reset_database()

    def ripe_core(self, names = None, base_url = None, reset = True):
        names = names or (
            "account.json",
            "availability_rule.json",
            "ddp_rules.json",
            "exchange_rates.json",
            "extra_duty_rules.json",
            "factory_rule.json",
            "hs_code_maps.json",
            "hs_code_rules.json",
            "letter_rule.json",
            "order_state.json",
            "order.json",
            "price_rule.json",
            "product.json",
            "shipping_rules.json"
        )

        base_url = base_url or "https://cdn.platforme.com/data/ripe_core/%s"

        api = self.export_api(
            base = self.core,
            ctx = "core"
        )

        if reset: self.reset(api = api)

        for name in names:
            model = os.path.splitext(name)[0]
            items = appier.get(base_url % name)
            data = dict(items = items)
            api.import_model(model, data)

    def ripe_retail(self, names = None, base_url = None, reset = True):
        names = names or (
            "account.json",
            "brand.json",
            "store.json",
            "retail_account.json"
        )

        base_url = base_url or "https://cdn.platforme.com/data/ripe_retail/%s"

        api = self.export_api(
            base = self.retail,
            ctx = "retail"
        )

        if reset: self.reset(api = api)

        for name in names:
            model = os.path.splitext(name)[0]
            items = appier.get(base_url % name)
            data = dict(items = items)
            api.import_model(model, data)

    def ripe_retail_dummy(self):
        self._ripe_retail_extra("dummy")

    def ripe_retail_sergio_rossi(self):
        self._ripe_retail_extra("sergio_rossi")

    def ripe_retail_emilio_pucci(self):
        self._ripe_retail_extra("emilio_pucci")

    @property
    def api(self):
        return self.export_api()

    def export_api(self, base = None, ctx = None):
        base = base or self.core
        ctx = ctx or "core"
        name = "_export_api_%s" % ctx
        if hasattr(self, name) and getattr(self, name):
            return getattr(self, name)
        export_api = appier_export.API(
            base_url = base.export_api_url + "/",
            admin_url = base.admin_api_url + "/",
            username = base.username,
            password = base.password
        )
        setattr(self, name, export_api)
        return export_api

    def admin_api(self, base = None, ctx = None):
        base = base or self.core
        ctx = ctx or "core"
        name = "_admin_api_%s" % ctx
        if hasattr(self, name) and getattr(self, name):
            return getattr(self, name)
        admin_api = appier_admin.API(
            base_url = base.admin_api_url + "/",
            username = base.username,
            password = base.password
        )
        setattr(self, name, admin_api)
        return admin_api

    def _ripe_retail_extra(self, brand):
        url_prefix = "https://cdn.platforme.com/data/ripe_retail_%s/" % brand
        self.ripe_retail(
            names = (
                "brand.json",
                "store.json",
                "retail_account.json"
            ),
            base_url = url_prefix + "%s",
            reset = False
        )
