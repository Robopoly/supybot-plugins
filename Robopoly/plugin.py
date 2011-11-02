###
# Copyright (c) 2011, Andrew Watson
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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import json

class Robopoly(callbacks.Plugin):
    """
    Robopoly is a group of commands that provide some functionality for the
    #robopoly channel on freenode. Most of these are wrappers around the
    Robopoly API.
    """
    threaded = True

    def sciper(self, irc, msg, args, number):
        """<sciper>

        Returns the name of the person associated with the given number
        """
        number = str(number)
        name = utils.web.getUrl('http://api.robopoly.ch/people/%s' % number)
        irc.reply("Number # " + number + " : " + name)
    sciper = wrap(sciper, ['int'])

    def tsol(self, irc, msg, args, direction, stop):
        """<direction> [<stop>]
        
        Tells you when the next metro leaves in <direction> (lausanne or renens).
        Optional parameter <stop> defaults to EPFL
        """
        if not stop:
            stop = "EPFL"
        url = 'http://api.robopoly.ch/tsol/%s/%s' % (stop, direction) 
        #irc.reply("Stop : %s and Direction : %s" % (stop, direction))
        #irc.reply(url)
        try:
            response = utils.web.getUrl(url)
            response = json.loads(response)
            formatstr = "Next TSOL from {stop} to {direction} in {n} minutes." + \
                        " Following one in {m} minutes."
            answer = formatstr.format(direction=direction, stop=stop,
                                        n=response[0], m=response[1])
        except:
            answer = "Error getting timetable from {stop} to {direction}."
            answer = answer.format(direction=direction, stop=stop)
        irc.reply(answer)
    tsol = wrap(tsol, ['something', optional('something')])

    def nowplaying(self, irc, msg, args, field):
        """[<field>]
        
        Returns artist - title of the track currently playing. Optionally,
        You can specify which field you want.
        """
        base_url = 'http://api.robopoly.ch/music/playing'
        if field is None:
            url = base_url
        else:
            url = base_url + "/" + field
        response = utils.web.getUrl(url)
        response = "Now playing at Robopoly : " + response
        irc.reply(response)
    nowplaying = wrap(nowplaying, [optional('something')])
    


Class = Robopoly


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
