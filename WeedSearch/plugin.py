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
import json

class WeedSearch(callbacks.Plugin):
    """This plugin parses leafly and returns the details of a weed strain on IRC."""
    threaded = True

    def strain(self, irc, msg, args, strain):
        """(strain <strain_name) -- Queries for details of a weed strain on leafly. For support, message aaa on EFnet."""
        try:
            channel = msg.args[0]
            strain = re.sub("[^\w\:\"\#\-\.' ]", "", strain).casefold()

            ########
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json;charset=utf-8',
                'Origin': 'https://www.leafly.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://www.leafly.com/search?q=kush&page=1',
                'TE': 'Trailers',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }

            data = {"params":{"lat": 0,"lon": 0,"q": strain,"skip":0,"take":7,"filter":{"type":["strain"]}}}
            response = requests.post('https://www.leafly.com/web-home/api/search', headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                irc.reply("Couldn't query leafly.com")
                return

            search_api = json.loads(response.text)
            strain_list = [i['slug'] for i in search_api['results']['strain']]

            if not strain_list:
                irc.reply('What have you been smoking?')
                return
            first_result = strain_list[0]
            url = 'https://www.leafly.com/strains/{}'.format(first_result)

            ########
            req2 = requests.get(url)
            if req2.status_code != 200:
                irc.reply("Couldn't query leafly.com")
                return

            soup2 = bs4.BeautifulSoup(req2.text, 'html.parser')

            name_tag = soup2.find('h1', {'itemprop': 'name'})
            if name_tag:
                name_text = 'Name: {}'.format(name_tag.text)
            else:
                name_text = ''

            thc_tag = soup2.find('button', {'class': 'text-xs bg-deep-green-20 py-sm px-sm rounded'})
            if thc_tag:
                thc_text = 'THC: {}'.format(thc_tag.text.split(' ')[1])
            else:
                thc_text = ''

            description_tag = soup2.find('div', {'itemprop': 'description'})
            if description_tag:
                description_text = 'Description: {}'.format(description_tag.text)
            else:
                description_text = ''

            effects_tag = soup2.find('div', {'class': 'react-tabs__tab-panel-container mt-md'})
            if effects_tag:
                effects = []
                for idx, effects_row in enumerate(effects_tag):
                    effects.append([])
                    for effect in effects_row:
                        effect_name = ' '.join(effect.div.text.split(' ')[:-1])
                        effect_percentage = effect.div.text.split(' ')[-1]
                        # effect_percentage = '\x0307{}\x03'.format(effect_percentage)
                        colored_effect = '{} {}'.format(effect_name, effect_percentage)
                        effects[idx].append(colored_effect)

                effects_string = []
                for effect_row in effects:
                    effects_string.append(', '.join(effect_row))
                effects_full_string = 'Feelings: {} Helps With: {} Negatives: {}'.format(*effects_string)
            else:
                effects_full_string = ''

            reply_string = ' '.join([name_text, thc_text, description_text, effects_full_string])

            irc.reply(reply_string)
        except Exception as e:
            irc.reply(f'Error { e }')

    strain = wrap(strain, ["text"])

Class = WeedSearch
