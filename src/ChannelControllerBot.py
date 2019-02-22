import time
import json

import telepot
from telepot.loop import MessageLoop

import SharedFunctions as sf
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
    channels = sf.OpenJson(name= "channels")
    channels[key] = 0 
    sf.SaveJson(name= "channels", data=channels)


def DeleteChannel(key):
    channels = sf.OpenJson(name= "channels")
    
    if key in channels:
        channels.pop(key, None)
        sf.SaveJson(name= "channels", data=channels)
        return True
    else:
        return False
    

def GetChannels():
    channels = sf.OpenJson(name= "channels")
    list_of_channels = ""
    for channel in channels:
        list_of_channels = list_of_channels + str(channel) + "\n"

    return list_of_channels


def ChangeEnableAds():
    ads = sf.OpenJson(name= "ads")

    if ads["enable"] == 1:
        ads["enable"] = 0
        ads_block_status = "disabled"
    else:
        ads["enable"] = 1
        ads_block_status = "enabled"

    sf.SaveJson(name= "ads", data=ads)

    return ads_block_status


def GetAdsRuleList():
    ads = sf.OpenJson(name= "ads")
    if ads["enable"] == 0:
        list_of_channels = "WARNING!\nAdBlock disabled\n"
    else:
        list_of_channels = ""
    for ad in ads:
        if ad != "enable":
            list_of_channels = list_of_channels + str(ad) + "\n"

    return list_of_channels


def AddRuleToList(rule):
    ads = sf.OpenJson(name="ads")
    ads[rule] = 0
    sf.SaveJson(name="ads", data=ads)


def DeleteRule(ad):
    ads = sf.OpenJson(name="ads")
    if ad in ads:
        ads.pop(ad, None)
        sf.SaveJson(name= "ads", data=ads)
        return True
    else:
        return False


def handle(msg):
    bot_username = bot.getMe()["username"]
    chat_id = msg['chat']['id']

    print("Msg from %s " % chat_id) #Channel id has "-". Keep it add to 

    if ( (config.admin_chat_id == None and config.channel_id == None) or chat_id == config.admin_chat_id or chat_id == config.channel_id):
        command = msg['text'].lower()

        command = command.split(" ")

        if ( len(command) == 1 ):
            if (command[0] == '/channels' or command[0] == '/channels@' + bot_username):
                list_of_channels = "Channels followed:\n\n" +  GetChannels()
                bot.sendMessage(chat_id, list_of_channels)

            elif (command[0] == '/setads' or command[0] == '/setads@' + bot_username):
                ads_block_status = ChangeEnableAds()
                bot.sendMessage(chat_id, "AdBlock %s" %ads_block_status)

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

            elif command[0] == '/addrule':
                    AddRuleToList( command[1].lower() )
                    bot.sendMessage(chat_id, "Successful add %s" % command[1])

            elif command[0] == '/delrule':

                result = DeleteRule(command[1])
                if (result):
                    bot.sendMessage(chat_id, "Successful delete %s" % command[1])
                else:
                    bot.sendMessage(chat_id, "Rule %s allready deleted" % command[1])

    else:
        print(chat_id)


isNotConn = True
while isNotConn:
    try:
        bot = telepot.Bot(config.bot_token)
        MessageLoop(bot, handle).run_as_thread()
        isNotConn = False
    except Exception as e:
        print(str(e))
        time.sleep(10)

while 1:
    time.sleep(10)