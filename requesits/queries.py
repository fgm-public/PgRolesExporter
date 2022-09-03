#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Gets role, source address and app name
# for each active query 
MULTI_QUERY = '''
    SELECT usename,client_addr,application_name 
    FROM   pg_stat_activity 
    WHERE  usename=$1 
    AND    datname=$2;
'''

# Gets roles list by DB
USENAMES_QUERY = '''
    SELECT usename
    FROM   pg_stat_activity 
    WHERE  datname=$1;
'''