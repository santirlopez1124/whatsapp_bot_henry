import pandas as pd
import sys, os
import datetime
# from sqlalchemy import create_engine

sys.path.insert(1,'../ayenda_bot_app_whatsapp/WebWhatsapp-Wrapper')
# Now do your import
from webwhatsapi import WhatsAPIDriver

def whatsapp_scraping(driver):
    all_chat_ids = driver.get_all_chat_ids()
    for j in range(len(all_chat_ids)):
        driver.delete_chat(all_chat_ids[j])

def contact_id(df):
    our_sims_ids = ['573054158965@c.us', '573053032694@c.us', '573244755031@c.us', '573244755013@c.us', '573013209450@c.us', '573052527680@c.us', '51910041368@c.us', '573004669489@c.us']
    df['contact_id'] = df.sender_id.where(~df.sender_id.isin(our_sims_ids), df.receiver_id)
    return df

if __name__ == '__main__':
    driver = WhatsAPIDriver('chrome')
    while True:
        if driver.get_status() == 'LoggedIn':
            conversations = whatsapp_scraping(driver)
            sys.path.insert(1,'../ayenda_bot_app_whatsapp/WebWhatsapp-Wrapper')
            driver.close()
            print('all messages are deleted')