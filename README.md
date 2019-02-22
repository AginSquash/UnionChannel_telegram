# Union Channel 
## What's it?

This is a simple program that will combine all your channels into one, as well as filter ads in them.

## How it works?

The program through your account goes to all the channels that you have added to the `channels.json` and sends them to your personal (or not) channel.
Subscribe to the channels in the telegrams is not required.

## How to use

+ Firstly, install all requirements with 
    >pip install -r requirements.txt
+ Go to my.telegram.org and create your own app (get your api_id and api_hash).
+ Create a channel where you want to see the news.
+ Create a bot with t.me/BotFather.
+ Now paste all data into `config.py`, like this:

      ###     Telegram-client side:   ###
      api_id = XXXX
      api_hash = "XXXXXXXXXXXXXXXXXXX"
      MyChannel = "XXXXXXXXXXXXXXXXXXXXXXXX" #link to your chat 
 
      ###          Bot-side:          ###
      bot_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      admin_chat_id = XXXXXXX       #Secure option. You can get this data into log-file. Optional.
      channel_id = -XXXXXXXXXX

+ On first start you must enter phone-number and password from telegram-account. Telethon requried.
