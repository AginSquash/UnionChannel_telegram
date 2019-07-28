import datetime
import json
import time
from random import randint
import logging

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import ImportChatInviteRequest

import SharedFunctions as sf
import config


def CheckSponsored(msg, KeyPharses):

    try:
        isAd = False
        for Pharse in KeyPharses:
            if msg.message.lower().find(Pharse)!=-1: 
                isAd = True
                logging.info("Message id " + str(msg.id) + " is Sponsored")
        if (isAd == False):
            return msg
        else: 
            return None
    except:
        msg

def OpenSponsored():
    ads = sf.OpenJson(name="ads")
    if ads["enable"]==1:
        ads_list = list()
        for ad in ads:
            if ad == "enable:":
                pass
            else:
                ads_list.append(ad)
        return ads_list
    else:
        return None
    



def ForwardMsg(client, peer, msgMassive, MyChannel):

    KeyPharse = OpenSponsored()
    messages_real = list()

    for msg in msgMassive:
        if KeyPharse != None:
            NeedToAdd = CheckSponsored(msg, KeyPharse)
            if NeedToAdd != None:
                messages_real.append(msg)
        else:
            messages_real.append(msg)

    grouped_msg_ids = list()
    msg_non_grupped = list()
    last_grrouped_id = -1
    messages_real.reverse()

    for msg in messages_real:
        if msg.grouped_id != None:
            if msg.grouped_id == last_grrouped_id:
                grouped_msg_ids.append(msg.id)
            else:
                if CheckTRUE(msg_non_grupped):
                    SendMsg(client, peer, msg_non_grupped, MyChannel)
                    msg_non_grupped = list()
                if CheckTRUE(grouped_msg_ids):
                    SendGroupped(client, peer, grouped_msg_ids, MyChannel)
                    grouped_msg_ids = list()
                last_grrouped_id = msg.grouped_id
                grouped_msg_ids.append(msg.id)
        else:
            if CheckTRUE(grouped_msg_ids):
                    SendGroupped(client, peer, grouped_msg_ids, MyChannel)
                    grouped_msg_ids = list()
            msg_non_grupped.append(msg.id)

    if CheckTRUE(msg_non_grupped):
        SendMsg(client, peer, msg_non_grupped, MyChannel)    

    if CheckTRUE(grouped_msg_ids):
        SendGroupped(client, peer, grouped_msg_ids, MyChannel)

    return  msgMassive[0].id 



def CheckTRUE(_list):
    if len(_list) > 0:
        return True
    else:
        return False

def SendMsg(client, peer, msg_non_grupped, MyChannel):
    client(functions.messages.ForwardMessagesRequest(
            from_peer = peer,
            id = msg_non_grupped,
            to_peer = MyChannel,
            with_my_score = True
        ))

def SendGroupped(client, peer, grupped_ids, MyChannel):
    client(functions.messages.ForwardMessagesRequest(
            from_peer = peer,
            id = grupped_ids,
            to_peer = MyChannel,
            with_my_score = True,
            grouped = True
        ))
    return grupped_ids

def GetHistory(client, min, channel_id):
    messages = client(functions.messages.GetHistoryRequest(
                peer=channel_id,
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=min,
                hash=0
              ))
    return messages.messages

def GetLastMsg(client, channel_id):
    messages = client(functions.messages.GetHistoryRequest(
                peer=channel_id,
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0
              ))
    return messages.messages[0].id



def OpenUpdateTime():
    return sf.OpenJson(name= "channels")

def SaveUpdateTime(key, LastMsg_id):
    channels = sf.OpenJson(name= "channels")
    channels[key] = LastMsg_id - 1 #
    sf.SaveJson(name="channels", data= channels)

def SaveNewTime(channels):
    print("SAVING: " + str(channels) )
    sf.SaveJson(name="channels", data= channels)

def Subs2PrivateChat(client, channel_id):
    ch = channel_id.split("/")
    req = ch[len(ch)-1]
    try:
        updates = client(ImportChatInviteRequest(req))
        client.edit_folder(updates.chats, 1)
    except:
        print("allready subs")

def main(client):
    needSave = False
    channels = OpenUpdateTime()
    MyChannel = config.MyChannel
    for channel_id in channels:
        if (channels[channel_id] == 0):
    
            if channel_id.find("t.me/joinchat")!= -1:
                Subs2PrivateChat(client, channel_id)

            LastMsg_id = GetLastMsg(client, channel_id)
            SaveUpdateTime(key = channel_id, LastMsg_id = LastMsg_id)
            channels = OpenUpdateTime()
        try:
            msg = GetHistory(client = client, min = channels[channel_id], channel_id = channel_id)
            print("(2) msg len: " + str( len(msg) ))
            print("(2) channels: " + str(channels) )
            print("(2) channels[channel_id]: " + str(channels[channel_id]) )

            if ( len(msg)> 0):
                LastMsg_id = ForwardMsg(client = client, peer = channel_id, msgMassive = msg, MyChannel = MyChannel)
                channels[channel_id] = LastMsg_id
                print("LastMsg_id: " + str(LastMsg_id) )
                needSave = True
            time.sleep(randint(5, 10))
        except Exception as e:
            logging.error( str(e) )
    
    if needSave:
        SaveNewTime(channels)
        client(functions.messages.MarkDialogUnreadRequest(
            peer = MyChannel,
            unread = True
        ))
        
    

if __name__ == '__main__':
    logging.basicConfig(filename="MainClient.log", level=logging.INFO)
    api_id = config.api_id
    api_hash = config.api_hash
    isNotConnected = True
    logging.info("Start")
    while isNotConnected:
        try:
            client = TelegramClient('UChannel', api_id, api_hash)
            client.start()
            isNotConnected = False
        except Exception as e:
            logging.error( str(e) )
            time.sleep(30)           
    wait = randint(5, 15)

    print("Starting in ", wait )
    time.sleep(wait)
    while True:
        try:
            main(client)
            wait = 180 # 3 min   
            print("Waiting for ", wait )
            time.sleep(wait)
        except Exception as e:
            print(str(e))
            time.sleep(30)