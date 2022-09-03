#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datatypes.pgrolesresult import DbCredentials

DB_CREDS = {
    'test_db_1': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-01-cluster.service.contoso.tech',
    ),
    'test_db_2': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-02-cluster.service.contoso.tech',
    ),
}