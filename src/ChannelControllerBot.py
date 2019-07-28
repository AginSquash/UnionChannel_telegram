import time
import json
import logging

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

import SharedFunctions as sf
import config

def CheckCorrectly(channel):
    channel = channel.replace("@", "https://t.me/")
    if channel.find("https://t.me/") == -1:
        channel = channel.replace("t.me/", "https://t.me/")
    if channel.find("https://t.me/") == -1:
        return "error"
    else:
        return channel

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


def ChangeEnableAds(isEnbale):
    ads = sf.OpenJson(name= "ads")

    if (isEnbale==None):
        if ads["enable"] == 1:
            ads["enable"] = 0
            ads_block_status = "disabled"
        else:
            ads["enable"] = 1
            ads_block_status = "enabled"
    else:
        if isEnbale == True:
            ads["enable"] = 1
            ads_block_status = "enabled"
        else:
            ads["enable"] = 0
            ads_block_status = "disabled"

    sf.SaveJson(name= "ads", data=ads)

    return ads_block_status


def GetAdsRuleList():
    ads = sf.OpenJson(name= "ads")
    if ads["enable"] == 0:
        list_of_channels = "*WARNING!\nAdBlock disabled*\n\n"
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

def CollectOtherText(commands):
    input_text = ""
    i = 0
    while i < len(commands):
        if i+1 == len(commands):
            input_text += commands[i]
        else:
            input_text += commands[i] + " "
        i += 1
    return input_text

class Bot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        bot_username = bot.getMe()["username"]
        chat_id = msg['chat']['id']

        print("Msg from %s " % chat_id) #Channel id has "-". Keep it add to 

        if ( (config.admin_chat_id == None and config.channel_id == None) or chat_id == config.admin_chat_id or chat_id == config.channel_id):
            
            try:
                command = msg['text']
                command = command.split(" ")
            except:
                command = "NoTextHere"
            if len(command)>1 and type(command) == list:
                if (command[1].find("https://t.me/joinchat/") == -1):
                    temp_list = list()

                    for cmd in command:
                        temp_list.append(cmd.lower())

                    command = temp_list
                    temp_list = None
                else:
                    command[0] = command[0].lower()

            if (command[0][0] == "/"):
                if ( len(command) == 1 ):
                    if (command[0] == '/channels' or command[0] == '/channels@' + bot_username):
                        list_of_channels = "Channels followed:\n\n" +  GetChannels()
                        bot.sendMessage(chat_id, list_of_channels)

                    elif (command[0] == '/setads' or command[0] == '/setads@' + bot_username):
                        ads_block_status = ChangeEnableAds(None)
                        bot.sendMessage(chat_id, "AdBlock %s" %ads_block_status)

                    elif (command[0] == '/rules' or command[0] == '/rules@' + bot_username):
                        ads_block_list = GetAdsRuleList()
                        bot.sendMessage(chat_id, text= "*AdBlock List*:\n\n" + ads_block_list, parse_mode="Markdown" ,reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Enable', callback_data='enable'),
                        InlineKeyboardButton(text='Disable', callback_data='disable'),
                            ]]))

                    else:
                        bot.sendMessage(chat_id, "Incorrect input")
                else:
                    if command[0] == '/add':
                        new_channel = CheckCorrectly(command[1])
                        if (new_channel != "error" ):
                            AddChannel(new_channel)
                            bot.sendMessage(chat_id, "Successful add %s" % new_channel)
                        else:
                            bot.sendMessage(chat_id, "Incorrect channel format")

                    elif command[0] == '/del':

                        result = DeleteChannel(command[1])
                        if (result):
                            bot.sendMessage(chat_id, "Successful delete %s" % command[1])
                        else:
                            bot.sendMessage(chat_id, "Channel %s allready unfollowed" % command[1])

                    elif command[0] == '/addrule':
                            input_text = CollectOtherText(command[1:len(command)])
                            print(input_text)
                            AddRuleToList( input_text )
                            bot.sendMessage(chat_id, "Successful add %s" % input_text)

                    elif command[0] == '/delrule':
                        input_text = CollectOtherText(command[1:len(command)])
                        result = DeleteRule(input_text)
                        if (result):
                            bot.sendMessage(chat_id, "Successful delete %s" % input_text)
                        else:
                            bot.sendMessage(chat_id, "Rule %s allready deleted" % input_text)

        else:
            logging.info("Unverifed chat: %s" % chat_id)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        if query_data == 'enable':
            ads_block_status = ChangeEnableAds(True)
        else:
            ads_block_status = ChangeEnableAds(False)

        self.bot.answerCallbackQuery(query_id, text= "AdBlock %s" % ads_block_status)


isNotConn = True
logging.basicConfig(filename="ChannelControllerBot.log", level=logging.INFO)
while isNotConn:
    try:
        bot = telepot.DelegatorBot(config.bot_token, [
            include_callback_query_chat_id(
                pave_event_space())(
                    per_chat_id(), create_open, Bot, timeout=900), #15 min
        ])
        MessageLoop(bot).run_as_thread()
        isNotConn = False
    except Exception as e:
        logging.error(str(e))
        time.sleep(10)

while 1:
    time.sleep(10)