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
            "factory_rule.json",
            "letter_rule.json",
            "order.json",
            "order_state.json",
            "price_rule.json",
            "product.json"
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
