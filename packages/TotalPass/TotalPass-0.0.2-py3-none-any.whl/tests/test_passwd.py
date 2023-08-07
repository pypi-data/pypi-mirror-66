#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import totalpass
from totalpass.passwd import Passwd


def test_passwd_str():
    passwd = Passwd(
        name="Cisco 1123", vendor="Cisco", category="snmp", comment="Just for test"
    )
    passwd.credentials.append(dict(username="user", password="cisco"))
    assert (
        str(passwd)
        == "Name: Cisco 1123, Category: snmp, Port: 0\nCredentials: [('user', 'cisco')]"
    )
