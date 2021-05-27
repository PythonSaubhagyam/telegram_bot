#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tested with Telethon version 1.14.0
from notifypy import Notify
import time
import sys
import configparser
from telethon import TelegramClient,functions, types
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
import json
import schedule 
import logging
import telegram 
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
# (1) Use your own values here
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

# (2) Create the client and connect
phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash)

async def main():
    await client.start()
    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

  
    while True:

        try:
            search = input('Which word you want to find :-')
            result = await client(functions.contacts.SearchRequest(
            # q = client.get_entity('hello'),
            q=search,
            # from_id = '797703540',
            limit=50
            )   )
       
            final_output = result.stringify()
            json_output = json.dumps(final_output,indent=4, sort_keys=True)
            print(json_output)
            bot = telegram.Bot(token='1887567751:AAFyxm6XI22Zhpk70G9lOr2dOurPF1ernZU')
            bot.sendMessage(chat_id='797703540', text=final_output)
    
        except KeyboardInterrupt:
            sys.exit(1)
        

with client:
    client.loop.run_until_complete(main())

# schedule.every(4).seconds.do(main())
# while 1:
#         schedule.run_pending()
#         time.sleep(1)