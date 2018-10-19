# -*- coding: utf-8 -*-
'''
    @license

    Copyright(c) 2018, Héctor Abraham Morillo Prieto and the project's contributors.

    This source code is licensed under the Apache License, Version 2.0 found in
    the LICENSE.txt file in the root directory of this source tree.
'''
import unittest
from autologin import AutoLogin


class TestAutoLogin(unittest.TestCase):
    def test_given_config_file_load_config_retrieves_correct_data(self):
        url, ssid = AutoLogin.load_config("../test/resources/config.json")
        self.assertEqual("wifi_ssid", ssid)
        self.assertEqual("login_url", url)

    def test_given_credentials_file_load_credentials_retrieves_correct_date(self):
        user, password = AutoLogin.load_credentials("../test/resources/credentials.json")
        self.assertEqual("user", user)
        self.assertEqual("password", password)

    if __name__ == '__main__':
        unittest.main()
