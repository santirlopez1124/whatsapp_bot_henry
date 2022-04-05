import pandas as pd
import time
import sys, os

sys.path.insert(1,'../ayenda_bot_reservations/WebWhatsapp-Wrapper')
# Now do your import
from webwhatsapi import WhatsAPIDriver

if __name__ == '__main__':
    driver = WhatsAPIDriver('chrome')
    while True:
        if driver.get_status() == 'LoggedIn':
            df = pd.read_csv('/Users/santirojas/Documents/ayenda/supply_experiment/prospectados_no_validated.csv')
            invalidos_1 = [['chat_id_1', 'status_1']]
            invalidos_2 = [['chat_id_2', 'status_2']]
            invalidos_3 = [['chat_id_3', 'status_3']]
            invalidos_4 = [['chat_id_4', 'status_4']]
            for i in range(len(df)):
                # if (type(df['chat_id_1'][i]) != str) or (type(df['chat_id_2'][i]) != str) or (type(df['chat_id_3'][i]) != str) or (type(df['chat_id_4'][i]) != str):
                #     continue
                # else:
                status_number_1 = driver.check_number_status(df['chat_id_1'][i]).get_js_obj()['status']
                status_number_2 = driver.check_number_status(df['chat_id_2'][i]).get_js_obj()['status']
                status_number_3 = driver.check_number_status(df['chat_id_3'][i]).get_js_obj()['status']
                status_number_4 = driver.check_number_status(df['chat_id_4'][i]).get_js_obj()['status']
                if status_number_1 == 200:
                    invalidos_1.append([df['chat_id_1'][i], 1])
                if status_number_1 == 404:
                    invalidos_1.append([df['chat_id_1'][i], 0])
                if status_number_2 == 200:
                    invalidos_2.append([df['chat_id_2'][i], 1])
                if status_number_2 == 404:
                    invalidos_2.append([df['chat_id_2'][i], 0])
                if status_number_3 == 200:
                    invalidos_3.append([df['chat_id_3'][i], 1])
                if status_number_3 == 404:
                    invalidos_3.append([df['chat_id_3'][i], 0])
                if status_number_4 == 200:
                    invalidos_4.append([df['chat_id_4'][i], 1])
                if status_number_4 == 404:
                    invalidos_4.append([df['chat_id_4'][i], 0])
            df_status_1 = pd.DataFrame(invalidos_1, columns=invalidos_1.pop(0))
            df_status_1.to_csv('/Users/santirojas/Documents/ayenda/supply_experiment/prospectados_validated_1.csv')
            df_status_2 = pd.DataFrame(invalidos_2, columns=invalidos_2.pop(0))
            df_status_2.to_csv('/Users/santirojas/Documents/ayenda/supply_experiment/prospectados_validated_2.csv')
            df_status_3 = pd.DataFrame(invalidos_3, columns=invalidos_3.pop(0))
            df_status_3.to_csv('/Users/santirojas/Documents/ayenda/supply_experiment/prospectados_validated_3.csv')
            df_status_4 = pd.DataFrame(invalidos_4, columns=invalidos_4.pop(0))
            df_status_4.to_csv('/Users/santirojas/Documents/ayenda/supply_experiment/prospectados_validated_4.csv')
            print(df_status_4.info())