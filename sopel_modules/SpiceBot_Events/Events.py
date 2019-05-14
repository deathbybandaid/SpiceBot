# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module
from sopel.trigger import PreTrigger

from .System import bot_events_trigger, bot_events_recieved, bot_events_startup_check, bot_events_setup_check, BotEvents
botevents = BotEvents()
from sopel_modules.SpiceBot_SBTools import bot_logging

import time


@sopel.module.event('001')
@sopel.module.rule('.*')
def bot_startup_connection(bot, trigger):
    bot_events_trigger(bot, botevents.BOT_WELCOME, "Welcome to the SpiceBot Events System")

    while not len(bot.channels.keys()) > 0:
        pass
    time.sleep(1)
    bot_events_trigger(bot, botevents.BOT_CONNECTED, "Bot Connected to IRC")


@sopel.module.event(botevents.BOT_WELCOME)
@sopel.module.rule('.*')
def bot_events_start(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    bot_events_recieved(bot, trigger.event)

    bot_events_trigger(bot, botevents.BOT_READY, "Ready To Process module setup procedures")

    while not bot_events_startup_check(bot):
        pass
    bot_events_trigger(bot, botevents.BOT_LOADED, "All registered modules setup procedures have completed")


@sopel.module.event(botevents.BOT_READY)
@sopel.module.rule('.*')
def bot_events_ready(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    bot_events_recieved(bot, trigger.event)


@sopel.module.event(botevents.BOT_CONNECTED)
@sopel.module.rule('.*')
def bot_events_connected(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    bot_events_recieved(bot, trigger.event)

    bot_events_setup_check(bot)

    while True:
        try:
            if len(bot.memory['SpiceBot_Events']["queue"]):
                number = bot.memory['SpiceBot_Events']["queue"][0]["number"]
                message = bot.memory['SpiceBot_Events']["queue"][0]["message"]
                pretrigger = PreTrigger(
                    bot.nick,
                    ":SpiceBot_Events " + str(number) + " " + str(bot.nick) + " :" + message
                )
                bot.dispatch(pretrigger)
                del bot.memory['SpiceBot_Events']["queue"][0]
        except KeyError:
            return


@sopel.module.event(botevents.BOT_LOADED)
@sopel.module.rule('.*')
def bot_events_complete(bot, trigger):
    bot_logging(bot, 'SpiceBot_Events', trigger.args[1], True)
    bot_events_recieved(bot, trigger.event)
