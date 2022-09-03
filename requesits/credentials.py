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
    'test_db_3': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-03-cluster.service.contoso.tech',
    ),
    'test_db_4': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-04-cluster.service.contoso.tech',
    ),
    'test_db_5': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-05-cluster.service.contoso.tech',
    ),            
    'test_db_6': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-06-cluster.service.contoso.tech',
    ),
    'test_db_7': DbCredentials(
        username='user',
        password='pa$$w0rd',
        bouncer_addr='pgbouncer.service.contoso.tech',
        direct_addr='master.dc-nsk-postgres-07-cluster.service.contoso.tech',
    ),
}
