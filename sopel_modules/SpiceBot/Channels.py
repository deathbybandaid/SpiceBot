# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
This is the SpiceBot Channels system.
"""
import sopel
import re


class BotChannels():
    """This Logs all channels known to the server"""
    def __init__(self):
        self.channel_lock = False
        self.SpiceBot_Channels = {
                                "list": {},
                                "InitialProcess": False
                                }

    def channel_list_request(self, bot):
        bot.write(['LIST'])

    def channel_list_recieve_start(self):
        self.channel_lock = True

    def channel_list_recieve_input(self, trigger):
        channel, _, topic = trigger.args[1:]
        if channel.lower() not in self.dict['list'].keys():
            self.dict['list'][channel.lower()] = dict()
        self.dict['list'][channel.lower()]['name'] = channel
        self.dict['list'][channel.lower()]['topic'] = self.topic_compile(topic)
        self.channel_lock = True

    def channel_list_recieve_finish(self):
        if not self.dict['InitialProcess']:
            self.dict['InitialProcess'] = True
        self.channel_lock = False

    def topic_compile(self, topic):
        actual_topic = re.compile(r'^\[\+[a-zA-Z]+\] (.*)')
        topic = re.sub(actual_topic, r'\1', topic)
        return topic

    def bot_part_empty(self, bot):
        """Don't stay in empty channels"""
        ignorepartlist = []
        if bot.config.core.logging_channel:
            ignorepartlist.append(bot.config.core.logging_channel)
        for channel in bot.channels.keys():
            if len(bot.channels[channel].privileges.keys()) == 1 and channel not in ignorepartlist and channel.startswith("#"):
                bot.part(channel, "Leaving Empty Channel")
                if channel.lower() in self.dict['list']:
                    del self.dict['list'][channel.lower()]

    def join_all_channels(self, bot):
        if bot.config.SpiceBot_Channels.joinall:
            for channel in self.dict['list'].keys():
                if channel.startswith("#"):
                    if channel not in bot.channels.keys() and channel not in bot.config.SpiceBot_Channels.chanignore:
                        bot.write(('JOIN', bot.nick, self.dict['list'][channel]['name']))
                        if channel not in bot.channels.keys() and bot.config.SpiceBot_Channels.operadmin:
                            bot.write(('SAJOIN', bot.nick, self.dict['list'][channel]['name']))

    def chanadmin_all_channels(self, bot):
        # Chan ADMIN +a
        for channel in bot.channels.keys():
            if channel.startswith("#"):
                if channel not in bot.config.SpiceBot_Channels.chanignore:
                    if bot.config.SpiceBot_Channels.operadmin:
                        if not bot.channels[channel].privileges[bot.nick] < sopel.module.ADMIN:
                            bot.write(('SAMODE', channel, "+a", bot.nick))
                else:
                    bot.part(channel)


channels = BotChannels()
