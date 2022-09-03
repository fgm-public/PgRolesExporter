#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pgpoll.pgpoll import PgRolesPoller
from requesits.test_sets import DB_CREDS
from requesits.credentials import DB_CREDS as _DB_CREDS
from datatypes.pgrolesresult import PgRolesResult
from utils.utils import patch_event_loop_policy


class TestPgRolesPoller(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
       self.pg_roles_poller = PgRolesPoller()


    async def test_handle_query_success(self):
        ''' Indirectly tests also:
                _get_query
                _make_query
                _get_roles
        '''
        in_fact = await self.pg_roles_poller._handle_query('test_db_1')
        expected = {'user', 'postgres'}

        self.assertEqual(set(in_fact), expected)


    async def test_handle_query_failed(self):
        ''' Indirectly tests also:
                _get_query
                _make_query
                _get_roles
        '''
        in_fact = await self.pg_roles_poller._handle_query('test_db_7')
        expected = [None]

        self.assertEqual(in_fact, expected)


    def test_form_results(self):
        # Delta between test credentials set and actual inventory credentials set
        creds_delta = len(_DB_CREDS) - len(DB_CREDS)

        missed_addrs = tuple('0.0.0.0' for i in range(creds_delta))
        addrs_test_set = ('172.28.140.240', '172.28.140.240') + missed_addrs

        missed_db = [[None] for i in range(creds_delta)]
        roles_test_set = [['user'], ['replicator']] + missed_db

        self.pg_roles_poller._form_results(roles_test_set, addrs_test_set)

        in_fact = self.pg_roles_poller.poll_result[:2]

        expected = [PgRolesResult(
                        db_name = "test_db_1",
                        roles = roles_test_set[0],
                        ip_addr = addrs_test_set[0],
                        direct_addr = DB_CREDS["test_db_1"].direct_addr,
                        bouncer_addr = DB_CREDS["test_db_1"].bouncer_addr,
                        poll_duration = 0,
                    ),
                    PgRolesResult(
                        db_name = "test_db_2",
                        roles = roles_test_set[1],
                        ip_addr = addrs_test_set[1],
                        direct_addr = DB_CREDS["test_db_2"].direct_addr,
                        bouncer_addr = DB_CREDS["test_db_2"].bouncer_addr,
                        poll_duration = 0,                        
                    )]

        self.assertEqual(in_fact, expected)


if __name__ == "__main__":
    patch_event_loop_policy()
    unittest.main()
