# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nose.tools

from . import cli_runner
from server import commands


def register_test():
    result = cli_runner.invoke(commands.run)
    nose.tools.assert_equal(result.exit_code, 0, "Command returned non-zero exit code")
    nose.tools.assert_equal(result.output, "Works!\n")
