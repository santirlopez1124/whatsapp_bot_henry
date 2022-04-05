import pandas as pd
import datetime 

our_sims_ids = ['573054158965@c.us', '573053032694@c.us', '573244755031@c.us', '573244755013@c.us', '573013209450@c.us', '573052527680@c.us', '573004669489@c.us', '573225168965@c.us', '573126055649@c.us', '573235351019@c.us']
        
# respondio descuento
def check_answered_discount(conversation):
    discount_msgs = conversation[conversation.text.str.lower().str.contains('descuento') & (conversation.sender_id.isin(our_sims_ids))]
    discount_question_datetime = '3013-01-01 00:00:00' if len(discount_msgs) == 0 else discount_msgs.iloc[0].datetime
    return ((conversation.datetime > discount_question_datetime) & (~conversation.sender_id.isin(our_sims_ids))).any()

# llegó mensaje inicial
def arrive_initial_message(conversation):
    initial_message = ['hola']
    for index, message in conversation.iterrows():
        if type(message.text) != str:
            continue
        if message.sender_id in our_sims_ids:
            if message.arrive_message == 2 or message.arrive_message == 3:
                if any([word in message.text.lower().split() for word in initial_message]):
                    return 1
    return 0

# solicitaron información descarga app
def need_contizacion(conversation):
    cotizacion = ['cotización']
    for index, message in conversation.iterrows():
        if type(message.text) != str:
            continue
        if message.sender_id in our_sims_ids:
            if any([word in message.text.lower().split() for word in cotizacion]):
                return 1
    return 0

# reservas
def reservation(conversation):
    reservation_condition = ['🛎']
    for index, message in conversation.iterrows():
        if type(message.text) != str:
            continue
        if message.sender_id in our_sims_ids:
            if any([word in message.text.lower().split() for word in reservation_condition]):
                return 1
    return 0

# error 
def error(conversation):
    confusion = ['equivocación', 'disculpas', 'error']
    error_2 = ['confusión', 'equivocada']
    for index, message in conversation.iterrows():
        if type(message.text) != str:
            continue
        if message.sender_id in our_sims_ids:
            if any([word in message.text.lower().split() for word in confusion]):
                return 1
        if message.sender_id not in our_sims_ids:
            if any([word in message.text.lower().split() for word in error_2]):
                return 1
    return 0

# solicitaron información descarga app
def info_about_app(conversation):
    download_app = ['google', 'store'] # 1
    for index, message in conversation.iterrows():
        if type(message.text) != str:
            continue
        if message.sender_id in our_sims_ids:
            if any([word in message.text.lower().split() for word in download_app]):
                return 1
    return 0


def merged_data(function, name, conversation):
    df = conversation.groupby('contact_id').apply(function)
    df.name = name
    conversation = conversation.merge(df.reset_index(), on='contact_id')
    return conversation

def percentages_analysis(conversation, column, condition, comparison, name):
    df = conversation[conversation[column] == condition]
    df_number = len(df)
    list_returned = [name, df_number, len(comparison)]
    return list_returned

def whatsapp_scraping(data, driver):
    conversations = [['sender_id', 'sender_name', 'text', 'isBusiness', 'isEnterprise', 'datetime', 'to_id', 'arrive_message']]
    # data = data[data['validos']==1]
    # data.reset_index(inplace=True, drop=True)
    scraped_users = []
    all_chat_ids = driver.get_all_chat_ids()
    for j in range(len(data)):
        if data['chat_id'][j] in all_chat_ids:
            scraped_users.append(j)
            driver.chat_load_all_earlier_messages(chat_id=data['chat_id'][j])
            messages = list(driver.get_all_messages_in_chat(data['chat_id'][j], include_me=True))
            # try:
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
            # except:
            #     pass
    scraping_table = pd.DataFrame(conversations, columns=conversations.pop(0))
    return scraping_table
    