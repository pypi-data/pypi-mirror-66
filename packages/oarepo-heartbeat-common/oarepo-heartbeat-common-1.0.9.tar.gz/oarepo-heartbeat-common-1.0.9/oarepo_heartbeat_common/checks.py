# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# oarepo-heartbeat-common is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Common heartbeat checks for OArepo instances."""
import time

from flask import current_app
from invenio_db import db
from invenio_search import current_search_client
from redis import StrictRedis
from sqlalchemy import text

from oarepo_heartbeat_common.errors import DatabaseUnhealthy


def check_db_health(*args, **kwargs):
    """Checks if configured DB is healthy."""
    query = text('SELECT COUNT(*) from alembic_version')

    try:
        t1 = time.time()
        res = db.engine.execute(query).fetchall()
        t2 = time.time()
        if len(res) != 1 or res[0] == 0:
            return 'database', False, {'error': str(DatabaseUnhealthy())}
        return 'database', True, {'time': t2 - t1}
    except Exception as e:
        return 'database', False, {'error': str(e)}


def check_db_readiness(*args, **kwargs):
    """Checks if configured DB is ready to accept connections."""
    try:
        t1 = time.time()
        db.session.execute('SELECT 1')
        t2 = time.time()
        return 'database', True, {'time': t2 - t1}
    except Exception as e:
        return 'database', False, {'error': str(e)}


def check_elasticsearch(*args, **kwargs):
    """Checks if configured ElasticSearch cluster is reachable."""
    try:
        t1 = time.time()
        current_search_client.indices.get_alias("*", request_timeout=10)
        t2 = time.time()
        return 'elasticsearch', True, {'time': t2 - t1}
    except Exception as e:
        return 'elasticsearch', False, {'error': str(e)}


def check_redis(*args, **kwargs):
    """Checks if configured Redis instance is pingable."""
    try:
        r = StrictRedis.from_url(current_app.config['CACHE_REDIS_URL'])
        t1 = time.time()
        res = r.ping()
        t2 = time.time()
        return 'redis', res, {'time': t2 - t1}
    except (ConnectionError, ValueError) as e:
        return 'redis', False, {'error': str(e)}
