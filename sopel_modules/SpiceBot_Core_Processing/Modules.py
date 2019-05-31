# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Modules system.
"""
import sopel

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event(SpiceBot.events.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):

    SpiceBot.events.startup_add([SpiceBot.events.BOT_COMMANDS])

    for comtype in SpiceBot.commands.dict['commands'].keys():
        if comtype not in ['module', 'nickname', 'rule']:
            SpiceBot.logs.log('SpiceBot_Commands', "Found " + str(len(SpiceBot.commands.dict['commands'][comtype].keys())) + " " + comtype + " commands.", True)

    SpiceBot.events.trigger(bot, SpiceBot.events.BOT_COMMANDS, "SpiceBot_Commands")