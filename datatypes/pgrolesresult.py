#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import (
    BaseModel, IPvAnyAddress
)


class PgRolesResult(BaseModel):
    '''Represents roles poll result for DB
    '''
    db_name: str
    roles: list
    ip_addr: IPvAnyAddress
    direct_addr: str
    bouncer_addr: str
    poll_duration: float


class DbCredentials(BaseModel):
    '''Represents connection credentials for DB
    '''    
    username: str
    password: str
    bouncer_addr: str
    direct_addr: str
