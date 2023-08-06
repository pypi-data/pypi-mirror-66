#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import unittest
from typing import Text

from procamora_utils.ip import IP


class TestIP(unittest.TestCase):

    def test_incorrect(self: TestIP):
        self.assertRaises(AttributeError, IP)

    def test_correct_fqdn(self: TestIP):
        fqdn: Text = 'test.com'
        ip: IP = IP(fqdn=fqdn)
        self.assertEqual(ip.get_addr(), fqdn, msg='not valid FQDN')

    def test_incorrect_fqdn(self: TestIP):
        fqdn: Text = 'test'
        self.assertRaises(AttributeError, IP, fqdn=fqdn)

    def test_correct_ip(self: TestIP):
        ipv4: Text = '192.168.1.1'
        ip: IP = IP(ip=ipv4)
        self.assertEqual(ip.get_addr(), str(ipv4), msg='not valid IP')

    def test_incorrect_ip(self: TestIP):
        self.assertRaises(AttributeError, IP, fqdn='192.168.1')


if __name__ == '__main__':
    unittest.main()
