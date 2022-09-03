#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from time import sleep

from prometheus_client import (
    start_http_server, Histogram, Gauge, Info
)

from datatypes.pgrolesresult import PgRolesResult
from pgpoll.pgpoll import PgRolesPoller
from requesits.credentials import DB_CREDS
from requesits.misc import EXP_PORT, POLL_INT
from utils.log import DEBUG_APP
from utils.utils import (
    patch_event_loop_policy, stats_collector
)


class PgRolesExporter():
    ''' Export active roles actually presented on postgres clusters
        and roles poll statistics in prometheus compatible format
    '''
    __slots__ = ("_poll_int", 
                 "_failed_polls", "_success_polls",
                 "_pg_roles_poller", "_exporter_info", 
                 "_poll_statistics", "_postgres_roles", 
                 "_inventory_count", "_roles_count")

    # Cluster specific labels names batch
    # for some metrics instances initialization
    init_labels = ('environment', 'application', 'component', 
                   'db_name', 'address', 'bouncer', 'instance')

    # General labels batch for all metrics instances
    static_labels = {"component": "psql_roles_exporter",
                     "application": "psql_roles_exporter", 
                     "environment": "production"}


    def __init__(self, poll_int: int=5):
        # Clusters polling interval
        self._poll_int = poll_int

        self._pg_roles_poller = PgRolesPoller()

        # Exporter info
        self._exporter_info = Info('exporter', 
                                  'Postgres clusters active roles poller')
        self._exporter_info.info(PgRolesExporter.static_labels)
        
        self._inventory_count = Gauge('inventory_count', 
                                      'Amount of clusters in inventory to be polled',
                                      PgRolesExporter.static_labels.keys())

        self._roles_count = Gauge('roles_count', 
                                  'Amount of unique roles on all inventoried databases', 
                                  PgRolesExporter.static_labels.keys())

        self._success_polls = Gauge('success_polls', 
                                    'Amount of successfully polled clusters', 
                                    PgRolesExporter.static_labels.keys())

        self._failed_polls = Gauge('failed_polls', 
                                   'Amount of cluster poll failures', 
                                   PgRolesExporter.init_labels)

        self._postgres_roles = Gauge('postgres_roles', 
                                     'Active postgres roles on clusters right now', 
                                     PgRolesExporter.init_labels + ('role',))

        self._poll_statistics = Histogram('poll_statistics',
                                          'Database poll statistics',
                                          PgRolesExporter.init_labels)


    def _form_dynamic_labels(self, db: PgRolesResult) -> dict:
        ''' Forms cluster specific labels
        '''
        dynamic_labels = {
            "db_name": db.db_name,
            "instance": db.direct_addr,
            "bouncer": db.bouncer_addr,
            "address": db.ip_addr,
        } 
        return PgRolesExporter.static_labels | dynamic_labels


    def _count_unique_roles(self) -> int:
        ''' Counts unique roles from all databases
        '''
        unique_roles = {role for db in self._pg_roles_poller.poll_result
                            for role in db.roles}
        return len(unique_roles)
        

    def _set_metrics(self) -> None:
        ''' Set metrics with fresh polled data
        '''
        inventory_count = len(DB_CREDS)
        self._inventory_count.labels(
            **PgRolesExporter.static_labels).set(inventory_count)

        roles_count = self._count_unique_roles()
        self._roles_count.labels(
            **PgRolesExporter.static_labels).set(roles_count)

        failed = 0
        for db in self._pg_roles_poller.poll_result:
            complete_labels = self._form_dynamic_labels(db)
            if len(db.roles): # successfully polled DB
                self._poll_statistics.labels(**complete_labels).observe(db.poll_duration)
                for role in db.roles:
                    self._postgres_roles.labels(**complete_labels, role=role,).set(1)
            else:
                self._failed_polls.labels(**complete_labels).set(1)
                failed += 1

        pooled_count = len(self._pg_roles_poller.poll_result) - failed
        self._success_polls.labels(
            **PgRolesExporter.static_labels).set(pooled_count)


    @stats_collector
    async def _intervaled_poll(self) -> None:
        ''' Polls clusters, stands for poll interval
        '''
        await asyncio.gather(
            asyncio.create_task(asyncio.sleep(self._poll_int)),
            asyncio.create_task(self._pg_roles_poller.poll_db_roles())
        )


    async def _refresh_metrics(self) -> None:
        ''' Spins process of metrics actualization  
        '''
        while True:
            await self._intervaled_poll()
            self._set_metrics()


    def start_export(self) -> None:
        asyncio.run(self._refresh_metrics(), debug=DEBUG_APP)


if __name__ == "__main__":
    app_metrics = PgRolesExporter(poll_int=POLL_INT)
    start_http_server(EXP_PORT)
    patch_event_loop_policy()
    app_metrics.start_export()
