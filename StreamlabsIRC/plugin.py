###
# Copyright (c) 2020, Triple A
# All rights reserved.
#
#
###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('StreamlabsIRC')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class StreamlabsIRC(callbacks.Plugin):
    """Uses Streamlabs API to play ASCII in IRC channels requested by donations."""
    threaded = True


Class = StreamlabsIRC


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
