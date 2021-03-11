###
# Copyright (c) 2021, aaa
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks, log
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Xtracter')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import requests

# lol bs4 can't use xpath
# https://stackoverflow.com/a/11466033
import lxml.html

class Xtracter(callbacks.Plugin):
    """Extracts text from a webpage based on XPath."""
    threaded = True

    def xtract(self, irc, msg, args, url, xpath):
        """[url] [xpath]

        Queries url and returns text from xpath.
        """
        response = requests.get(url, stream = True)
        response.raw.decode_content = True

        tree = lxml.html.parse(response.raw)
        tags = tree.xpath(xpath)

        if len(tags) == 0:
            irc.reply("No results found.")
            return

        tag = tags[0]

        # https://stackoverflow.com/a/11963661
        result_text = tag.text_content()
        
        #TODO format this properly
        irc.reply(result_text)

    xtract = wrap(xtract, ["httpUrl", "text"])

Class = Xtracter


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
