# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from colorama import Fore, Back
import click
import os
from pep3143daemon import DaemonContext, PidFile
import zmq


import server
from core import config as core_config


@click.group()
@click.option('-c', '--config')
@click.pass_context
def cli(context, config):
    context.obj['config'] = core_config.read('server', os.path.dirname(server.__file__), config)
    pass


def register():
    cli(obj={})


@cli.command()
@click.option('-D','--daemon/--no-daemon', default=False)
@click.option('-d', '--dry-run/--no-dry-run', default=False)
@click.pass_context
def run(ctx, daemon, dry_run):
    config = ctx.obj['config']

    def main():
        click.echo(Fore.GREEN + 'Starting server...' + Fore.RESET)
        context = zmq.Context()

        # Socket to talk to clients
        publisher = context.socket(zmq.PUB)
        # set SNDHWM, so we don't drop messages for slow subscribers
        publisher.sndhwm = config.core.publish_high_watermark
        publisher.bind(config.core.publish_addres)
        click.echo(('Listening on: ' + Fore.YELLOW + '{}' + Fore.RESET).format(config.core.publish_addres))

        # Socket to receive signals
        syncservice = context.socket(zmq.REP)
        syncservice.bind(config.core.sync_addres)
        click.echo(('Synchronising on: ' + Fore.YELLOW + '{}' + Fore.RESET).format(config.core.sync_addres))

        if dry_run:
            click.echo(Fore.GREEN + 'Stopping server...' + Fore.RESET)
            return 0

        # Get synchronization from subscribers
        subscribers = 0
        while subscribers < 3:
            # wait for synchronization request
            msg = syncservice.recv()
            # send synchronization reply
            syncservice.send(b'')
            subscribers += 1
            click.echo("+1 subscriber (%i/%i)" % (subscribers, 3))

        # Now broadcast exactly 1M updates followed by END
        for i in range(1000000):
            publisher.send(b'Rhubarb')

        publisher.send(b'END')

        click.echo(Fore.GREEN + 'Stopping server...' + Fore.RESET)

        return 0

    if daemon:
        pid_file = PidFile(config.core.pid_file)
        with DaemonContext(pidfile=pid_file):
            return main()
    else:
            return main()
