# -*- coding: utf-8 -*-
'''
    @license

    Copyright(c) 2018, Héctor Abraham Morillo Prieto and the project's contributors.

    This source code is licensed under the Apache License, Version 2.0 found in
    the LICENSE.txt file in the root directory of this source tree.
'''

import os
import json
from selenium import webdriver
from time import sleep

CONFIG_FILE_PATH = "./config.json"
CREDENTIALS_PATH = "./credentials.json"
RETRIES_KILL_CAPTIVE_WINDOW = 10
WAIT_TIME_TO_KILL_CAPTIVE_WINDOW = 1
RETRIES_FOR_NETWORK = 10
WAIT_TIME_FOR_NETWORK = 1
LOGIN_DELAY = 1
WAIT_TIME_FOR_OPEN_CAPTIVE_WINDOW = 1


def restart_wifi():
    os.system("networksetup -setairportpower airport off")
    os.system("networksetup -setairportpower airport on")


def get_ssid_network_connected():
    return os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I "
                    "| awk -F': ' '/ SSID/ {print $2}'").read()


def wait_for_network(retries, wait_time_seconds, wifi_ssid):
    ssid = get_ssid_network_connected()
    if wifi_ssid in ssid:
        print("Wifi: ", ssid, " DETECTED!")
        return True
    elif retries > 0:
        print("Waiting for network, REMAINING RETRIES ", retries)
        sleep(wait_time_seconds)
        return wait_for_network(retries - 1, wait_time_seconds)
    else:
        return False


def kill_captative_process(retries, wait_time_seconds):
    process_id = os.popen("ps -x | pgrep \"Captive Network Assistant\"").read()
    if not process_id:
        print("Captive window NOT found, nothing to KILL! - REMAINING RETRIES", retries)
        if retries > 0:
            sleep(wait_time_seconds)
            return kill_captative_process(retries - 1, wait_time_seconds)
        else:
            return False
    else:
        print("Captive process is: ", process_id)
        print("Killing captive process...")
        os.system("kill -9 " + process_id)
        return True


def login(user, password, login_url):
    driver = webdriver.Safari()
    driver.get(login_url)
    sleep(LOGIN_DELAY)
    driver.find_element_by_id("user.username").send_keys(user)
    driver.find_element_by_id("user.password").send_keys(password)
    driver.find_element_by_id("ui_login_signon_button").click()
    sleep(LOGIN_DELAY)
    driver.find_element_by_id("ui_post_access_continue_button").click()
    sleep(LOGIN_DELAY * 2)
    driver.close()


def load_config(path):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("Config file exists and is readable")

        with open(path, "r") as data_file:
            data_loaded = json.load(data_file)

        return data_loaded["login_url"], data_loaded["wifi_ssid"]
    else:
        print("Either the config file is missing or not readable, please add a \\config.json")


def load_credentials(path):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("Credentials file exists and is readable")

        with open(path, "r") as data_file:
            data_loaded = json.load(data_file)

        return data_loaded["user"], data_loaded["password"]
    else:
        print("Either the credentials file is missing or not readable")


if __name__ == '__main__':
    loaded_login_url, loaded_wifi_ssid = load_config(CONFIG_FILE_PATH)
    if not loaded_login_url or not loaded_wifi_ssid:
        pass

    restart_wifi()
    if wait_for_network(RETRIES_FOR_NETWORK, WAIT_TIME_FOR_NETWORK, loaded_wifi_ssid):
        sleep(WAIT_TIME_FOR_OPEN_CAPTIVE_WINDOW)
        print("Trying to killing captive login...")
        kill_captative_process(RETRIES_KILL_CAPTIVE_WINDOW, WAIT_TIME_TO_KILL_CAPTIVE_WINDOW)

        print("Trying to login...")
        login(load_credentials(CREDENTIALS_PATH), loaded_login_url)
    else:
        print("WIFI Network not connected")
