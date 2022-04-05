import re

import pandas as pd


def input_variables(input_user, df):
    contact_messages = pd.DataFrame()
    new_input = ''
    res = re.findall('\w+|[^\s\w]+', input_user)
    input_user_splited = res
    list_columns_compared = [
        item for item in input_user_splited if item in list(df.columns)]
    for item in input_user_splited:
        if item in list_columns_compared:
            new_input += ' ' + df[item].apply(str)
        else:
            new_input += ' ' + item
    if type(new_input) != str:
        new_input = new_input.apply(lambda x: re.sub("\s*(\W)\s*", r"\1", x))
        new_input = new_input.str.replace(',', ', ')
        new_input = new_input.str.replace('!', '! ')
        new_input = new_input.str.replace('¡', ' ¡')
        new_input = new_input.str.replace('¿', ' ¿')
        new_input = new_input.str.replace('.', '. ')
        new_input = new_input.str.replace('?', '? ')
        new_input = new_input.str.strip()
    else:
        new_input = new_input.replace(',', ', ')
        new_input = new_input.replace('!', '! ')
        new_input = new_input.replace('¡', '¡ ')
        new_input = new_input.replace('¿', '¿ ')
        new_input = new_input.replace('.', '. ')
        new_input = new_input.replace('?', '? ')
        new_input = new_input.strip()
    contact_messages['contact_id'] = df['chat_id']
    contact_messages['message_sended_ab'] = new_input
    return contact_messages
