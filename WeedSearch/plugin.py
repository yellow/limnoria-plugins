###
# Copyright (c) 2020, TRIPLE A
# All rights reserved.
#
#
###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('WeedSearch')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import requests
import bs4
import re

class WeedSearch(callbacks.Plugin):
    """This plugin parses leafly and returns the details of a weed strain on IRC."""
    threaded = True

    def strain(self, irc, msg, args, strain):
        """function searches for weed strain on leafly"""
        channel = msg.args[0]
        strain = re.sub("[^\w\:\"\#\-\.' ]", "", strain).casefold()

        req = requests.get('https://www.leafly.com/search?q={}'.format(strain))
        if req.status_code != 200:
            irc.reply("Couldn't query leafly.com")
            return

        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        first_result = soup.find('a', {'class': 'jsx-3613316329'})

        if not first_result:
            irc.reply("Couldn't find your strain")
            return

        url = first_result['href']

        req2 = requests.get(url)
        if req2.status_code != 200:
            irc.reply("Couldn't query leafly.com")
            return

        soup2 = bs4.BeautifulSoup(req2.text, 'html.parser')

        thc_tag = soup2.find('button', {'class': 'flex font-mono font-bold flex-row items-center ml-md'})
        if thc_tag:
            thc = thc_tag.div.text
        else:
            thc = '--%'
        

        description = soup2.find('div', {'class': 'md:mb-xxl strain__description'}).p.text

        effects_soup = soup2.find('div', {'class': 'react-tabs__tab-panel-container mt-md'})
        if not effects_soup:
            irc.reply('\x02\x0309THC\x03\x02: \x0307{}\x03 \x02DESCRIPTION\x02: {}'.format(thc, description).replace('\xa0', ' '))
            return

        effects = []
        for idx, effects_row in enumerate(effects_soup):
            effects.append([])
            for effect in effects_row:
                effect_name = ' '.join(effect.div.text.split(' ')[:-1])
                effect_percentage = effect.div.text.split(' ')[-1]
                effect_percentage = '\x0307{}\x03'.format(effect_percentage)
                colored_effect = '{} {}'.format(effect_name, effect_percentage)
                effects[idx].append(colored_effect)

        effects_string = []
        for effect_row in effects:
            effects_string.append(', '.join(effect_row))
        print(effects_string)

        irc.reply('\x02\x0309THC\x03\x02: \x0307{}\x03 \x02DESCRIPTION\x02: {} \x02\x0311EFFECTS\x03\x02: \x02\x0306Feelings\x03\x02: {} \x02\x0309Helps with\x03\x02: {} \x02\x0304Negatives\x03\x02: {}'.format(thc, description, *effects_string).replace('\xa0', ' '))

    strain = wrap(strain, ["text"])

Class = WeedSearch
