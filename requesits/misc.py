#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Exporter listen port
EXP_PORT = 8009

# DB poll interval
POLL_INT = 10

# Static connection params
CONN_PARAMS = {
    "port": 5432,
    "command_timeout": 60,
    "server_settings": {"application_name": "role_check"}
}
