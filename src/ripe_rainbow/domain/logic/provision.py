#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_admin
import appier_export

from .. import parts

class ProvisionPart(parts.Part):

    _CACHE = {}

    @classmethod
    def _get(cls, url, cache = True):
        if cache and url in cls._CACHE: return cls._CACHE[url]
        cls._CACHE[url] = appier.get(url)
        return cls._CACHE[url]

    @classmethod
    def _clear(cls):
        cls._CACHE.clear()

    def reset(self, api = None, base = None, ctx = None):
        api = api or self.export_api(base = base, ctx = ctx)
        api.reset_database()

    def ripe_all_restore(self, reset = True):
        self.ripe_core_restore(reset = reset)
        self.ripe_retail_restore(reset = reset)

    def ripe_core(self, names = None, base_url = None, reset = True):
        cls = self.__class__

        names = names or (
            "account.json",
            "availability_rule.json",
            "country_group.json",
            "ddp_rules.json",
            "exchange_rate.json",
            "extra_duty_rule.json",
            "factory_rule.json",
            "hs_code_map.json",
            "hs_code_rule.json",
            "justifications.json",
            "letter_rule.json",
            "order_state.json",
            "order.json",
            "price_rule.json",
            "product.json",
            "shipping_rule.json"
        )

        base_url = base_url or "https://cdn.platforme.com/data/ripe_core/%s"

        api = self.export_api(base = self.core, ctx = "core")

        tuples = [(name, cls._get(base_url % name)) for name in names]

        if reset: self.reset(api = api)

        for name, items in tuples:
            model = os.path.splitext(name)[0]
            data = dict(items = items)
            api.import_model(model, data)

    def ripe_core_reset(self):
        self.reset(base = self.core, ctx = "core")

    def ripe_core_restore(self, reset = True):
        if reset: self.ripe_core_reset()
        self.ripe_core_minimal(reset = False)

    def ripe_core_minimal(self, names = None, base_url = None, reset = True):
        return self.ripe_core(
            names = names or ("account.json", ),
            base_url = base_url or "https://cdn.platforme.com/data/ripe_core_minimal/%s",
            reset = reset
        )

    def ripe_retail(self, names = None, base_url = None, reset = True):
        cls = self.__class__

        names = names or (
            "account.json",
            "brand.json",
            "store.json",
            "retail_account.json"
        )

        base_url = base_url or "https://cdn.platforme.com/data/ripe_retail/%s"

        api = self.export_api(base = self.retail, ctx = "retail")

        tuples = [(name, cls._get(base_url % name)) for name in names]

        if reset: self.reset(api = api)

        for name, items in tuples:
            model = os.path.splitext(name)[0]
            data = dict(items = items)
            api.import_model(model, data)

    def ripe_retail_reset(self):
        self.reset(base = self.retail, ctx = "retail")

    def ripe_retail_restore(self, reset = True):
        if reset: self.ripe_retail_reset()
        self.ripe_retail_minimal(reset = False)

    def ripe_retail_minimal(self, names = None, base_url = None, reset = True):
        return self.ripe_retail(
            names = names or ("account.json", ),
            base_url = base_url or "https://cdn.platforme.com/data/ripe_retail_minimal/%s",
            reset = reset
        )

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

    def _ripe_retail_extra(self, brand, reset = False):
        url_prefix = "https://cdn.platforme.com/data/ripe_retail_%s/" % brand
        self.ripe_retail(
            names = (
                "brand.json",
                "store.json",
                "retail_account.json"
            ),
            base_url = url_prefix + "%s",
            reset = reset
        )
