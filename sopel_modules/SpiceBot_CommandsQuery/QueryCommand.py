# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel
import sopel.module

import sopel_modules.SpiceBot as SpiceBot

import spicemanip


@SpiceBot.events.check_ready([SpiceBot.events.BOT_COMMANDSQUERY])
@sopel.module.rule('^\?(.*)')
def query_detection(bot, trigger):

    triggerargs, triggercommand = SpiceBot.sopel_triggerargs(bot, trigger, 'query_command')

    # command issued, check if valid
    if not triggercommand or not len(triggercommand):
        return

    if not SpiceBot.letters_in_string(triggercommand):
        return

    commands_list = dict()
    for commandstype in SpiceBot.commands.dict['commands'].keys():
        if commandstype not in ['rule', 'nickname']:
            for com in SpiceBot.commands.dict['commands'][commandstype].keys():
                if com not in commands_list.keys():
                    commands_list[com] = SpiceBot.commands.dict['commands'][commandstype][com]

    if triggercommand[:-1] == "+":

        triggercommand = triggercommand[:-1]
        if not triggercommand or not len(triggercommand):
            return

        if triggercommand.lower() not in list(commands_list.keys()):
            dispmsg = ["Cannot find any alias commands: No valid commands match " + str(triggercommand) + "."]
            closestmatches = SpiceBot.similar_list(bot, triggercommand, list(commands_list.keys()), 10, 'reverse')
            if len(closestmatches):
                dispmsg.append("The following commands match " + str(triggercommand) + ": " + spicemanip.main(closestmatches, 'andlist') + ".")
            bot.notice(dispmsg, trigger.nick)
            return

        realcom = triggercommand
        if "aliasfor" in commands_list[triggercommand].keys():
            realcom = commands_list[triggercommand]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        bot.notice("The following commands match " + str(triggercommand) + ": " + spicemanip.main(validcomlist, 'andlist') + ".", trigger.nick)
        return

    if triggercommand[:-1] == "?":

        triggercommand = triggercommand[:-1]
        if not triggercommand or not len(triggercommand):
            return

        closestmatches = SpiceBot.similar_list(bot, triggercommand, list(commands_list.keys()), 10, 'reverse')
        if not len(closestmatches):
            bot.notice("Cannot find any similar commands for " + str(triggercommand) + ".", trigger.nick)
        else:
            bot.notice("The following commands may match " + str(triggercommand) + ": " + spicemanip.main(closestmatches, 'andlist') + ".", trigger.nick)
        return

    commandlist = []
    for command in list(commands_list.keys()):
        if command.lower().startswith(str(triggercommand).lower()):
            commandlist.append(command)

    if not len(commandlist):
        bot.notice("No commands start with " + str(triggercommand) + ".", trigger.nick)
    else:
        bot.notice("The following commands start with " + str(triggercommand) + ": " + spicemanip.main(commandlist, 'andlist') + ".", trigger.nick)
