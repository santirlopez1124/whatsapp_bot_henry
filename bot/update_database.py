import pandas as pd
import sys, os
import datetime
# from sqlalchemy import create_engine

sys.path.insert(1,'../ayenda_bot_app_whatsapp/WebWhatsapp-Wrapper')
# Now do your import
from webwhatsapi import WhatsAPIDriver

def whatsapp_scraping(driver):
    conversations = [['sender_id', 'sender_name', 'body_conversation', 'is_whatsapp_business', 'is_whatsapp_enterprise', 'date_message', 'receiver_id', 'arrive_message']]
    scraped_users = []
    all_chat_ids = driver.get_all_chat_ids()
    for j in range(len(all_chat_ids)):
        scraped_users.append(j)
        driver.chat_load_all_earlier_messages(chat_id=all_chat_ids[j])
        messages = list(driver.get_all_messages_in_chat(all_chat_ids[j], include_me=True))
        # driver.delete_chat(all_chat_ids[j])
        #try:
        for i in range(len(messages)):
            text = messages[i].get_js_obj()['body']
            whatsapp_business = messages[i].get_js_obj()['chat']['contact']['isBusiness']
            is_enterprise = messages[i].get_js_obj()['chat']['contact']['isEnterprise']
            sender_id = messages[i].get_js_obj()['sender']['id']
            sender_name = messages[i].get_js_obj()['sender']['name']
            to_id = messages[i].get_js_obj()['to']
            date = datetime.datetime.fromtimestamp(messages[i].get_js_obj()['timestamp'])
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            arrive_message = messages[i].get_js_obj()['ack']
            conversations.append([sender_id, sender_name, text, whatsapp_business, is_enterprise, date, to_id, arrive_message])
        #except:
        #    pass
    scraping_table = pd.DataFrame(conversations, columns=conversations.pop(0))
    return scraping_table

def contact_id(df):
    our_sims_ids = ['573054158965@c.us', '573053032694@c.us', '573244755031@c.us', '573244755013@c.us', '573013209450@c.us', '573052527680@c.us', '51910041368@c.us', '573004669489@c.us']
    df['contact_id'] = df.sender_id.where(~df.sender_id.isin(our_sims_ids), df.receiver_id)
    return df

# def update_database(df):
#     cnxn = create_engine("postgresql+psycopg2://growth:9d26c01f69ccb3a9c4acefdeb4f54344@142.93.4.35:5432/whatsapp_conversations")
#     df.to_sql("growth_conversations", con=cnxn, schema="public", if_exists='append', index=False)

if __name__ == '__main__':
    driver = WhatsAPIDriver('chrome')
    while True:
        if driver.get_status() == 'LoggedIn':
            conversations = whatsapp_scraping(driver)
            df = contact_id(conversations)
            sys.path.insert(1,'../ayenda_bot_app_whatsapp/WebWhatsapp-Wrapper')
            df.to_csv('../ayenda_bot_app_whatsapp/databases/whatsapp_conversations_save_1.csv')
            # update_database(df)
            driver.close()
            print('the updating of database is finished')
