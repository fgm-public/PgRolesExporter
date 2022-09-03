#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import asyncpg

from datatypes.pgrolesresult import DbCredentials
from utils.utils import stats_collector
from utils.log import LOGGING_CONFIG
from requesits.credentials import DB_CREDS
from requesits.misc import CONN_PARAMS


class PgFetcher():
    ''' Represents postgres database object 
        Provides interface for async SQL queries
        with connection pooling
    '''
    __slots__ = ("_db_name", 
                 "_db_creds", "_common_params",
                 "_pg_pool", "_logger")

    def __init__(self, db_name):
        self._db_name = db_name
        self._db_creds: DbCredentials = DB_CREDS[db_name]
        self._common_params = CONN_PARAMS
        # Postgres connection pool
        self._pg_pool: asyncpg.pool.Pool | None = None
        logging.config.dictConfig(LOGGING_CONFIG)
        self._logger = logging.getLogger('pg_poll')


    def _get_params(self) -> dict:
        ''' Forms database connection params
        '''
        db_params = {
            "database": self._db_name,
            "host": self._db_creds.bouncer_addr,
            "user": self._db_creds.username,
            "password": self._db_creds.password,
        } 
        return db_params | self._common_params


    @stats_collector
    async def _init_connection_pool(self):
        ''' Initializing connection pool
        '''
        if not self._pg_pool:
            try:
                self._pg_pool = await asyncpg.create_pool(**self._get_params())
                self._logger.info(f'Connection pool for {self._db_name} initialized')
            except Exception as e:
                self._logger.exception(
                    f'Connection pool for {self._db_name} initialization FAILED! '
                    f'reason: {e}'
                )


    @stats_collector
    async def make_query(self, query: str) -> list[asyncpg.Record] | None:
        ''' Making a query to the database
        '''
        if not self._pg_pool:
            await self._init_connection_pool()
        try:
            async with self._pg_pool.acquire() as connection:
                async with connection.transaction():
                    response = await connection.fetch(query, self._db_name)
            self._logger.debug(f'Response from {self._db_name} is: {response}')
            return response
        except Exception as e:
            self._logger.exception(f'Query to {self._db_name} FAILED! reason: {e}')
