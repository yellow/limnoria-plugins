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

from supybot import ircmsgs
import websocket
import json
import pprint
import time
import threading
import os

class StreamlabsIRC(callbacks.Plugin):
    """Uses Streamlabs API to play ASCII in IRC channels requested by donations."""
    threaded = True

    def scroll(self, ascii_name, donor_name, donation_amount):
        print('scroll')

        ascii_filename = ascii_name + '.txt'

        if ascii_filename in os.listdir(self.ascii_directory):
            print(ascii_name + ': ascii_found')
            self.irc.queueMsg(ircmsgs.privmsg(self.channel_name, '{} has requested the "{}" ascii by donating {}'.format(donor_name, ascii_name, donation_amount)))
            print(os.path.join(self.ascii_directory, ascii_filename))
            with open(os.path.join(self.ascii_directory, ascii_filename), 'r') as f:
                for line in f.read().split('\n'):
                    self.irc.queueMsg(ircmsgs.privmsg(self.channel_name, line))
        else:
            self.irc.queueMsg(ircmsgs.privmsg(self.channel_name, '"{}" ascii not found :<'.format(ascii_name)))

    def stream_sock(self):
        def on_message(ws, message):
            if 'event' not in message:
                return

            first_square_bracket_index = message.find('[')

            if first_square_bracket_index == -1:
                return

            message_list_string = message[first_square_bracket_index:]
            message_list = json.loads(message[first_square_bracket_index:])

            if message_list[1]['type'] != 'donation':
                return

            pprint.pprint(message_list)

            donor_name = message_list[1]['message'][0]['from']
            donation_amount = message_list[1]['message'][0]['formatted_amount']
            donation_message = message_list[1]['message'][0]['message']

            if donation_message.startswith('!ascii '):
                self.scroll(donation_message.split('!ascii ')[1], donor_name, donation_amount)
                # self.scroll('vap0r-trex', donor_name, donation_amount)
            else:
                self.irc.queueMsg(ircmsgs.privmsg(self.channel_name, '{} donated {} with the message "{}"'.format(donor_name, donation_amount, donation_message)))

        def on_error(ws, error):
            print(error)

        def on_close(ws):
            print("### closed ###")


        def on_open(ws):
            print("### open ###")
            def run(*args):
                count = 0
                while True:
                    print('ping {}'.format(count))
                    count += 1
                    ws.send("2")
                    time.sleep(15)
            self.ws_ping = threading.Thread(target= lambda: run())
            self.ws_ping.daemon = False
            self.ws_ping.start()

        print('stream_sock')

        # websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp("wss://sockets.streamlabs.com/socket.io/?token={}&EIO=3&transport=websocket".format(self.streamlabs_socket_token), on_message = on_message, on_error = on_error, on_close = on_close)
        self.ws.on_open = on_open
        self.wst = threading.Thread(target=lambda: self.ws.run_forever())
        self.wst.daemon = False
        self.wst.start()

    def __init__(self, irc):
        print('__init__')
        self.ascii_directory = ""
        self.channel_name = ""
        self.streamlabs_socket_token = ""
        print(self.ascii_directory, self.channel_name, self.streamlabs_socket_token)
        self.irc = irc
        self.__parent = super(StreamlabsIRC, self)
        self.__parent.__init__(irc)
        self.stream_sock()
 
Class = StreamlabsIRC


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
