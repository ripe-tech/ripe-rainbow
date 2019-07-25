#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeRetailPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.login_url)

        form = self.driver.find_element(".form")
        username_input = form.find_element_by_name("username")
        self.driver.write_text(username_input, username)
        password_input = form.find_element_by_name("password")
        self.driver.write_text(password_input, password)
        self.driver.press_enter(password_input)

    def login_wait(self, username, password):
        self.login(username, password)
        self.waits.redirected_to(self.next_url)



    def select_size(self, size, gender = None, scale = None, open = True):
        return self.commons.select_size(
            size,
            gender = gender,
            scale = scale,
            open = open
        )

    def set_part(
            self,
            brand,
            model,
            part,
            material,
            color,
            part_text = None,
            material_text = None,
            color_text = None,
            verify = True,
            click_material = True,
            container_selector = ".content"
    ):
        return self.commons.set_part(
            brand,
            model,
            part,
            material,
            color,
            part_text if part_text else part.upper(),
            material_text = material_text,
            color_text = color_text,
            verify = verify,
            click_material = click_material,
            container_selector = container_selector
        )

    def assert_part(
            self,
            brand,
            model,
            part,
            material,
            color,
            part_text = None,
            material_text = None,
            color_text = None
    ):
        return self.commons.assert_part(
            brand,
            model,
            part,
            material,
            color,
            part_text = part_text,
            material_text = material_text,
            color_text = color_text
        )

    @property
    def retail_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-retail-ci.platforme.com")
        base_url = appier.conf("RETAIL_URL", base_url)
        base_url = appier.conf("RIPE_RETAIL_URL", base_url)
        return base_url

    @property
    def base_url(self):
        return self.retail_url

    @property
    def home_url(self):
        return "%s/" % self.retail_url

    @property
    def next_url(self):
        return self.home_url

    @property
    def login_url(self):
        return "%s/login" % self.retail_url

    @property
    def logout_url(self):
        return "%s/logout" % self.retail_url
