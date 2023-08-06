#!/usr/bin/env python

import logging

import click

from quakestats import (
    manage,
)
from quakestats.core.collector import (
    QLStatCollector,
)
from quakestats.health import (
    HealthInfo,
)
from quakestats.system import (
    conf,
    log,
)

logger = logging.getLogger(__name__)


# TODO consider moving to separate CLI module
@click.group()
def cli():
    pass


@cli.command(name="set-admin-pwd")
@click.argument("password")
def set_admin_password(password):
    # TODO find a good way to initialize DB access of the webapp
    from quakestats.web import mongo_db

    manage.set_admin_password(mongo_db.db, password)


@cli.command(name="rebuild-db")
def run_rebuild_db():
    from quakestats.web import data_store

    # TODO at the moment config is too closely bound to flask app
    result = manage.rebuild_db(
        conf.get_conf_val("RAW_DATA_DIR"),
        conf.get_conf_val("SERVER_DOMAIN"),
        data_store,
    )
    logger.info("Processed {} matches".format(result))


@cli.command(name="collect-ql")
@click.argument("host")
@click.argument("port")
@click.argument("password")
def collect_ql(host, port, password):
    from quakestats.core.ql import QLGame, MatchMismatch
    from quakestats.web import data_store

    game = QLGame()
    data_dir = conf.get_conf_val("RAW_DATA_DIR")
    server_domain = conf.get_conf_val("SERVER_DOMAIN")

    def event_cb(timestamp: int, event: dict):
        nonlocal game
        try:
            ev = game.add_event(timestamp, event)
        except MatchMismatch:
            logger.info(
                "Got game %s with %s events",
                game.game_guid, len(game.ql_events)
            )
            if game.ql_events:
                if data_dir:
                    manage.store_game(game, 'QL', data_dir)

                try:
                    manage.process_game(server_domain, game, data_store())
                except Exception as e:
                    logger.error('Failed to process match %s', game.game_guid)
                    logger.exception(e)

            game = QLGame()
            ev = game.add_event(timestamp, event)

        if ev:
            logger.debug("%s -> %s", ev.data['MATCH_GUID'], ev.type)

    collector = QLStatCollector(host, port, password)
    collector.read_loop(event_cb)


@cli.command(name="load-ql-game")
@click.argument('file_path')
def load_ql_game(file_path):
    from quakestats.web import data_store
    server_domain, game = manage.load_game(file_path)
    manage.process_game(server_domain, game, data_store())


@cli.command()
def status():
    colormap = {
        0: "green",
        1: "blue",
        2: "yellow",
        3: "red",
        4: "red",
    }

    health_info = HealthInfo()
    health = health_info.run()
    for key, val in health.items():
        click.echo(key + ": ", nl=False)
        level, comment = val
        click.secho(comment, fg=colormap[level])


def main(args=None):
    log.configure_logging(logging.DEBUG)
    cli()


if __name__ == "__main__":
    main()
