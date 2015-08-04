# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import click
import time
import zmq
from pep3143daemon import DaemonContext, PidFile


@click.group()
def cli():
    pass


def register():
    cli()


@cli.command()
def run():
    pid_file = PidFile('/tmp/server.pid')

    with DaemonContext(pidfile=pid_file):
        click.echo('Daemon starting...')
        context = zmq.Context()

        # First, connect our subscriber socket
        subscriber = context.socket(zmq.SUB)
        subscriber.connect('tcp://localhost:5561')
        subscriber.setsockopt(zmq.SUBSCRIBE, b'')

        time.sleep(1)

        # Second, synchronize with publisher
        syncclient = context.socket(zmq.REQ)
        syncclient.connect('tcp://localhost:5562')

        click.echo('Synchronizing')

        # send a synchronization request
        syncclient.send(b'')

        # wait for synchronization reply
        syncclient.recv()

        click.echo('Synchronizing - done')

        # Third, get our updates and report how many we got
        nbr = 0
        while True:
            msg = subscriber.recv()
            if msg == b'END':
                break
            nbr += 1

        click.echo('Received %d updates' % nbr)
