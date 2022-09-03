#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import asyncio

import aiodns

from utils.utils import stats_collector, TtlCache
from utils.log import LOGGING_CONFIG, DEBUG_APP


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('pg_poll')


@TtlCache
@stats_collector
async def resolve_dns(dns_name: str, ttl_hash=None) -> str:
    ''' Resolve DNS name to IP address
    '''        
    resolver = aiodns.DNSResolver()
    try: # resolve via DNS server
        response = await resolver.query(dns_name, 'A')
        ip_addr = response[0].host
        logger.debug(f'Resolved {dns_name} to {ip_addr} via DNS server')
    except aiodns.error.DNSError:
        try: # resolve via hosts file
            response = await resolver.gethostbyname(dns_name, 0)
            ip_addr = response.addresses[0]
            logger.debug(f'Resolved {dns_name} to {ip_addr} via hosts file')
        except aiodns.error.DNSError:
            ip_addr = '0.0.0.0'
            logger.exception(f'Cannot resolve {dns_name}')

    return ip_addr


if __name__ == "__main__":
    
    from requesits.credentials import DB_CREDS
    from utils.utils import (
        patch_event_loop_policy, print_runtime_statistics
    )

    @stats_collector
    async def main():
        resolve_tasks = [asyncio.create_task(
                            resolve_dns(DB_CREDS[db_name].direct_addr))
                                for db_name in DB_CREDS]
        responses = await asyncio.gather(*resolve_tasks)

    patch_event_loop_policy()
    asyncio.run(main(), debug=DEBUG_APP)

    print_runtime_statistics('Resolves', resolve_dns)
    print_runtime_statistics('Main', main)
    