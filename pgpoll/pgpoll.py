#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import asyncio

import asyncpg

from dnsresolver.dnsresolver import resolve_dns
from pgfetcher.pgfetcher import PgFetcher
from datatypes.pgrolesresult import PgRolesResult
from utils.utils import stats_collector
from utils.log import LOGGING_CONFIG, DEBUG_APP
from requesits.credentials import DB_CREDS
from requesits.queries import USENAMES_QUERY


class PgRolesPoller():
    ''' Poll active roles actually presented on postgres clusters
        Forms polled data object for prometheus exporter
    '''
    __slots__ = ("poll_result", "_databases", "_logger")


    def __init__(self):
        # Final results of polling for all processed databases
        self.poll_result: list[PgRolesResult] = []
        
        self._databases = {db_name: PgFetcher(db_name) 
                              for db_name in DB_CREDS}
        
        logging.config.dictConfig(LOGGING_CONFIG)
        self._logger = logging.getLogger('pg_poll')


    async def _prepare_poll(self):
        ''' Sets instance to another poll iteration
        '''
        if self.poll_result:
            self.poll_result = []
            self._logger.debug('Prepare to another poll...')


    def _get_query_tasks(self) -> list[asyncio.Task]:
        '''Forms list of asyncio tasks from SQL query coroutines
        '''
        return [asyncio.create_task(self._handle_query(db_name))
                    for db_name in DB_CREDS]


    def _get_resolve_tasks(self) -> list[asyncio.Task]:
        '''Forms list of asyncio tasks from DNS resolving coroutines
        '''        
        return [asyncio.create_task(
                    resolve_dns(DB_CREDS[db_name].direct_addr))
                            for db_name in DB_CREDS]


    def _get_roles(self, raw_response: list[asyncpg.Record]) -> list[str]:
        ''' Refining the database response
        '''
        return [row.get('usename') 
                    for row in tuple(set(raw_response))]


    @stats_collector
    async def _handle_query(self, db_name: str) -> list[str] | list[None]:
        '''Makes some intermediate actions and formattings
        '''
        raw_roles = await self._databases[db_name].make_query(USENAMES_QUERY)
        if raw_roles is not None:
            roles: list[str] = self._get_roles(raw_roles)
        else:
            roles = [None]
        self._logger.debug(f'{db_name} roles is: {roles}')            
        return roles


    def _get_query_duration(self, db_name: str) -> float:
        ''' Forms SQL query duration
        '''
        return round(
            self._databases[db_name].make_query.durations.get(db_name, 0), 2)


    def _form_results(self, roles: tuple[list[str]], addrs: tuple[str]) -> None:
        ''' Formatting and saving the final result to the instance result var
        '''
        for count, db_name in enumerate(DB_CREDS):
            result = {
                "db_name": db_name,
                "ip_addr": addrs[count],
                "direct_addr": DB_CREDS[db_name].direct_addr,
                "bouncer_addr": DB_CREDS[db_name].bouncer_addr,
                "roles": [],
                "poll_duration": 0
            }
            if not None in roles[count]:
                result['roles'] = [role for role in roles[count]]
                result['poll_duration'] = self._get_query_duration(db_name)
                self._logger.info(f'Database {db_name} polled')
            self.poll_result.append(PgRolesResult(**result))


    @stats_collector
    async def poll_db_roles(self) -> None:
        ''' Launch tasks for processing requests
        '''
        await self._prepare_poll()

        results = await asyncio.gather(
            *self._get_query_tasks(), 
            *self._get_resolve_tasks()
        )

        roles: tuple[list[str]] = results[:len(results)//2]
        addrs: tuple[str] = results[len(results)//2:]

        # Final formatting and saving the result
        self._form_results(roles, addrs)
        self._logger.debug(self.poll_result)


if __name__ == "__main__":

    from utils.utils import (
        print_runtime_statistics, patch_event_loop_policy
    )

    pg_roles_poller = PgRolesPoller()
    
    patch_event_loop_policy()
    asyncio.run(pg_roles_poller.poll_db_roles(), debug=DEBUG_APP)

    print(pg_roles_poller.poll_result)

    print_runtime_statistics('Resolves', resolve_dns)
    print_runtime_statistics('Main', pg_roles_poller.poll_db_roles)
