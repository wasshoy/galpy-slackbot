from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import random
import letstalk as lt

@respond_to('(.*)')
def get_message(message, arg):
    rep = lt.interface(arg)
    message.reply(rep)

@respond_to('(.*)がんばる')
def doit_func(message, arg):
    # リアクションスタンプを押す
    message.react('do_it_01')
    message.reply('ふぁいと〜😉👍')