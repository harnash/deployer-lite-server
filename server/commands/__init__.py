# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click


@click.command()
def register():
    click.echo("Works!")

    return 0
