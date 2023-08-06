#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import unittest

from procamora_utils.ip import IP
from procamora_utils.ping import ping


class TestIP(unittest.TestCase):

    def test_ip_up(self: TestIP):
        ip: IP = IP(ip='127.0.0.1')
        self.assertTrue(ping(ip), msg=f'{ip.get_addr()} must be up')

    def test_ip_down(self: TestIP):
        ip: IP = IP(ip='192.168.1.87')
        self.assertFalse(ping(ip), msg=f'{ip.get_addr()} must be down')

    def test_fqdn_up(self: TestIP):
        ip: IP = IP(fqdn='google.es')
        self.assertTrue(ping(ip), msg=f'{ip.get_addr()} must be up')

    def test_fqdn_down(self: TestIP):
        ip: IP = IP(fqdn='google.false')
        self.assertFalse(ping(ip), msg=f'{ip.get_addr()} must be down')


if __name__ == '__main__':
    unittest.main()
