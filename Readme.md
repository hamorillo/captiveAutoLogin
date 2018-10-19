# Auto Login Script
[![Build Status](https://travis-ci.org/hmorillo/captiveAutoLogin.svg?branch=master)](https://github.com/hmorillo/captiveAutoLogin)

This script make easier the login with captive credentials window.

## Dependencies
* Python 3.6 or 3.7
* Selenium
* Safari

## How to install
I assume that you have HomeBrew... If you don't have it go here and enjoy it :)
``https://brew.sh/index_es``

You can install HomeBrew with:
``/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"``

If you don't have Python 3.6 or 3.7 install it:
``brew install python3``

Install selenium dependency in Python:
``python3 -m pip install selenium``

On Safari app you have to enable **Remote Automation**, you can do it in following this steps:
* Safari -> Preferences
* In advance submenu, enable "Show Develop menu in menu bar"
* Close *Preferences* windows
* Open *Develop* menu and click on *Allow Remote Automation* 

You have to write a json file with name **credentials.json** in the same directory as *AutoLogin.py* with your WiFi credentials. The JSON file must have the following structure:

`` {
        "user": "wifi_user",
        "password": "wifi_password"
    }``

The script needs a **config.json** file in which you have to specify the login URL:

`` {
    "wifi_ssid": "WiFiSSID",
    "login_url": "https://login_captive.html"
}
``

## How to use
For running the script you only need to execute in your terminal:

``python3 AutoLogin.py``
    