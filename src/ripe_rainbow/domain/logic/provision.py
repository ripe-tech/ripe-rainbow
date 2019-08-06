#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_export

from .. import parts

class ProvisionPart(parts.Part):

    def ripe_core(self, data_set = None):
        names = (
            "account.json",
            "availability_rule.json",
            "factory_rule.json",
            "letter_rule.json",
            "order.json",
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
        if hasattr(self, "_api") and self._api: return self._api
        self._api = appier_export.API()
        return self._api
