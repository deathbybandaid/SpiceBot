# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from .gifsearch import getGif

import sopel.module

import spicemanip

from sopel_modules.SpiceBot.Tools import sopel_triggerargs
from sopel_modules.SpiceBot.Events import botevents


@botevents.check_ready([botevents.BOT_GIFSEARCH])
@sopel.module.commands('(.*)')
def gifapi_triggers(bot, trigger):

    triggerargs, triggercommand = sopel_triggerargs(bot, trigger, 'prefix_command')

    if triggercommand not in bot.memory["SpiceBot_GifSearch"]['valid_gif_api_dict'].keys():
        return

    if not len(triggerargs):
        return bot.osd("Please present a query to search.")

    query = spicemanip.main(triggerargs, 0)
    searchdict = {"query": query, "gifsearch": triggercommand}

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        bot.osd(gifdict["error"])
    else:
        bot.osd(str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"])))
