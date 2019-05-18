#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

from sopel_modules.SpiceBot_Logs.Logs import botlogs


def setup(bot):
    botlogs.log('SpiceBot_DatabaseCache', "Setting up Database Cache")
    if 'SpiceBot_DatabaseCache' not in bot.memory:
        bot.memory['SpiceBot_DatabaseCache'] = dict()


def shutdown(bot):
    if "SpiceBot_DatabaseCache" in bot.memory:
        del bot.memory["SpiceBot_DatabaseCache"]
