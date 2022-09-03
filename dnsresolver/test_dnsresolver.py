#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from dnsresolver.dnsresolver import resolve_dns
from requesits.test_sets import DB_CREDS
from utils.utils import patch_event_loop_policy


class TestNameResolver(unittest.IsolatedAsyncioTestCase):

    async def test_resolve_dns_hosts(self):

        hosts_addr = DB_CREDS["test_db_1"].direct_addr

        in_fact = await resolve_dns(hosts_addr)
        expected = '172.19.95.243'

        self.assertEqual(in_fact, expected)


    async def test_resolve_dns_server(self):

        name = 'koms.ru'
        
        in_fact = await resolve_dns(name)
        expected = '95.216.68.125'

        self.assertEqual(in_fact, expected)


    async def test_resolve_dns_failed(self):

        name = 'komsz.ru'
        
        in_fact = await resolve_dns(name)
        expected = '0.0.0.0'

        self.assertEqual(in_fact, expected)


if __name__ == "__main__":
    patch_event_loop_policy()
    unittest.main()
