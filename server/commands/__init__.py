# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click
import zmq
from pep3143daemon import DaemonContext, PidFile


@click.group()
def cli():
    pass


def register():
    cli()


@cli.command()
@click.option('-D','--daemon/--no-daemon', default=False)
@click.option('-d', '--dry-run/--no-dry-run', default=False)
def run(daemon, dry_run):
    def main():
        context = zmq.Context()

        # Socket to talk to clients
        publisher = context.socket(zmq.PUB)
        # set SNDHWM, so we don't drop messages for slow subscribers
        publisher.sndhwm = 1100000
        publisher.bind('tcp://*:5561')

        # Socket to receive signals
        syncservice = context.socket(zmq.REP)
        syncservice.bind('tcp://*:5562')

        if dry_run:
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

        return 0

    if daemon:
        pid_file = PidFile('/tmp/server.pid')
        with DaemonContext(pidfile=pid_file):
            click.echo('Daemon starting...')
            return main()
    else:
            return main()
