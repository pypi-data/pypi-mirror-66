# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# oarepo-heartbeat-common is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Common heartbeat checks for OArepo instances."""
import click
from flask.cli import with_appcontext

from oarepo_heartbeat_common.checks import check_db_health, \
    check_db_readiness, check_elasticsearch, check_redis
from oarepo_heartbeat_common.errors import DatabaseUninitialized


@click.group()
def heartbeat():
    """Heartbeat check commands."""


@heartbeat.group()
def readiness():
    """Readiness check command group."""


@heartbeat.group()
def liveliness():
    """Liveliness check command group."""


def _print_health_result(status, details=None):
    if details:
        err = details.get('error', None)
    else:
        err = None

    if status:
        click.echo('healthy')
    elif DatabaseUninitialized().description in err:
        click.echo('uninitialized')
    else:
        click.echo('unhealthy')


def _print_ready_result(status):
    if status:
        click.echo('ready')
    else:
        click.echo('not_ready')


@liveliness.command('db')
@with_appcontext
def db_healthy():
    """Checks if configured DB is healthy."""
    _, status, err = check_db_health()
    _print_health_result(status, err)


@liveliness.command('es')
@with_appcontext
def es_healthy():
    """Checks if configured ElasticSearch cluster is healthy."""
    _, status, _ = check_elasticsearch()
    _print_health_result(status)


@liveliness.command('redis')
@with_appcontext
def redis_healthy():
    """Checks if configured Redis instance is healthy."""
    _, status, details = check_redis()
    _print_health_result(status, details)


@readiness.command('db')
@with_appcontext
def db_ready():
    """Checks if configured DB is ready to accept connections."""
    _, status, _ = check_db_readiness()
    _print_ready_result(status)


@readiness.command('es')
@with_appcontext
def es_ready():
    """Checks if configured ElasticSearch cluster is ready."""
    _, status, _ = check_elasticsearch()
    _print_ready_result(status)


@readiness.command('redis')
@with_appcontext
def redis_ready():
    """Checks if configured Redis instance is ready to accept connections."""
    _, status, _ = check_redis()
    _print_ready_result(status)
