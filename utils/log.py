#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.config

DEBUG_APP = False

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(name)s: %(module)s: %(funcName)s: %(levelname)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'pg_poll': {
            'handlers': ['stream_handler'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
