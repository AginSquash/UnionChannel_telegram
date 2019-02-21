import time
import json

import telepot
from telepot.loop import MessageLoop

import config

def CheckCorrectly(channel):
    if (channel.find("t.me/") == -1):
        if (channel.find("@") == -1):
            return False
        else: 
            return True
    else: 
        return True

def AddChannel(key):
    with open('data/channels.json', 'r') as f:
            channels = json.load(f)
    channels[key] = 0 
    with open('data/channels.json', 'w') as f:
                json.dump(channels, f)

def DeleteChannel(key):
    with open('data/channels.json', 'r') as f:
            channels = json.load(f)
    
    if key in channels:
        channels.pop(key, None)
        with open('data/channels.json', 'w') as f:
                    json.dump(channels, f)
        return True
    else:
        return False
    
def GetChannels():
    with open('data/channels.json', 'r') as f:
        channels = json.load(f)
    list_of_channels = ""
    for channel in channels:
        list_of_channels = list_of_channels + str(channel) + "\n"

    return list_of_channels

def handle(msg):
    bot_username = bot.getMe()["username"]
    chat_id = msg['chat']['id']

    print("Msg from %s " % chat_id) #Channel id has "-". Keep it add to 

    if ( (config.admin_chat_id == None and config.channel_id == None) or chat_id == config.admin_chat_id or chat_id == config.channel_id):
        command = msg['text']

        command = command.split(" ")

        if ( len(command) == 1 ):
            if (command[0] == '/channels' or command[0] == '/channels@' + bot_username):
                list_of_channels = "Channels followed:\n\n" +  GetChannels()
                bot.sendMessage(chat_id, list_of_channels)
            else:
                bot.sendMessage(chat_id, "Incorrect input")
        else:
            if command[0] == '/add':
                if (CheckCorrectly( command[1]) ):
                    AddChannel(command[1])
                    bot.sendMessage(chat_id, "Successful add %s" % command[1])
                else:
                    bot.sendMessage(chat_id, "Incorrect channel format")
            elif command[0] == '/del':

                result = DeleteChannel(command[1])
                if (result):
                    bot.sendMessage(chat_id, "Successful delete %s" % command[1])
                else:
                    bot.sendMessage(chat_id, "Channel %s allready unfollowed" % command[1])
    else:
        print(chat_id)
isNotConn = True
while isNotConn:
    try:
        bot = telepot.Bot(config.bot_token)
        MessageLoop(bot, handle).run_as_thread()
        isNotConn = False
    except:
        time.sleep(10)

while 1:
    time.sleep(10)