###
# Copyright (c) 2020, TripleA
# All rights reserved.
#
#
###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('EtymologySearch')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


import requests
import bs4

class EtymologySearch(callbacks.Plugin):
    """Scrapes etymonline.com to get word etymology"""
    threaded = True

    def etym(self, irc, msg, args, etym):
        """queries etymonline.com for word etymology"""

        try:
            req = requests.get("https://www.etymonline.com/word/{}".format(etym))

            soup = bs4.BeautifulSoup(req.text, 'html.parser')

            word_soup = soup.find('div', {'class': 'word--C9UPa'})
            if not word_soup:
                irc.reply("'{}' not found".format(etym))
                return

            irc_reply = ""
            for word in word_soup:
                irc_reply += "{}: {} ".format(word.div.h1.text, word.div.section.text)
            print(irc_reply)

            irc.reply(irc_reply)

        except Exception as e:
            print(e)
            irc.reply("Error! Send the log to Druid@Freenode")

    etym = wrap(etym, ["text"])

Class = EtymologySearch


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
