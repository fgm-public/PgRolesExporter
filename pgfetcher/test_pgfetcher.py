#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import asyncpg

from pgfetcher.pgfetcher import PgFetcher
from requesits.test_sets import DB_CREDS
from requesits.misc import CONN_PARAMS
from requesits.queries import USENAMES_QUERY
from utils.utils import patch_event_loop_policy


class TestPgFetcher(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
       self.pg_fetcher = PgFetcher('test_db_1')


    async def test_get_params(self):

        in_fact = self.pg_fetcher._get_params()

        expected = {
            "database": 'test_db_1',
            "host": DB_CREDS['test_db_1'].bouncer_addr,
            "user": DB_CREDS['test_db_1'].username,
            "password": DB_CREDS['test_db_1'].password,
        } | CONN_PARAMS

        self.assertEqual(in_fact, expected)


    async def test_init_connection_pool(self):

        await self.pg_fetcher._init_connection_pool()
        in_fact = self.pg_fetcher._pg_pool
        
        self.assertIsInstance(in_fact, asyncpg.pool.Pool)


    async def test_make_query(self):

        raw_roles = await self.pg_fetcher.make_query(USENAMES_QUERY)
        in_fact = set(row.get('usename') for row in tuple(set(raw_roles)))

        expected = {'postgres', 'user'}

        self.assertEqual(in_fact, expected)


if __name__ == "__main__":
    patch_event_loop_policy()
    unittest.main()
