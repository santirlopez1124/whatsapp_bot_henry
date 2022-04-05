import pandas as pd
import time
import sys, os
import datetime

sys.path.insert(1,'../ayenda_bot_reservations/WebWhatsapp-Wrapper')
# Now do your import
from webwhatsapi import WhatsAPIDriver

if __name__ == '__main__':
    # driver = WhatsAPIDriver('chrome')
    # while True:
    #     if driver.get_status() == 'LoggedIn':
    #         chat = driver.get_chat_from_id('573204398958@c.us')
    #         # date = datetime.datetime.strptime('2021-10-03',"%Y-%m-%d")
    #         # timestamp = datetime.datetime.timestamp(date)
    #         # chat.load_earlier_messages_till(date)
    #         message = list(chat.get_messages(include_me=True))
    #         text = message[0].get_js_obj()['body']
    #         print(text)
    print(pd.__version__)

