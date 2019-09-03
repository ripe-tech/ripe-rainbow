#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_admin
import appier_export

from .. import parts

class ProvisionPart(parts.Part):

    def reset(self):
        self.admin_api.reset_database()

    def ripe_core(self, data_set = None):
        names = (
            "account.json",
            "availability_rule.json",
            "factory_rule.json",
            "letter_rule.json",
            "order.json",
            "order_state.json",
            "price_rule.json",
            "product.json"
        )

        base_url = "https://cdn.platforme.com/data/ripe_core/%s"

        for name in names:
            model = os.path.splitext(name)[0]
            items = appier.get(base_url % name)
            data = dict(items = items)
            self.api.import_model(model, data)

    def ripe_retail(self, data_set = None):
        names = (
            "brand.json",
            "store.json",
            "retail_account.json"
        )

        base_url = "https://cdn.platforme.com/data/ripe_retail/%s"

        for name in names:
            model = os.path.splitext(name)[0]
            items = appier.get(base_url % name)
            data = dict(items = items)
            self.api.import_model(model, data)

    @property
    def api(self):
        return self.export_api

    @property
    def export_api(self):
        if hasattr(self, "_export_api") and self._export_api: return self._export_api
        self._export_api = appier_export.API(
            base_url = self.core.export_api_url + "/",
            admin_url = self.core.admin_api_url + "/",
            username = self.core.username,
            password = self.core.password
        )
        return self._export_api

    @property
    def admin_api(self):
        if hasattr(self, "_admin_api") and self._admin_api: return self._admin_api
        self._admin_api = appier_admin.API(
            base_url = self.core.admin_api_url + "/",
            username = self.core.username,
            password = self.core.password
        )
        return self._admin_api
