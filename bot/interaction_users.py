import pandas as pd
import time
import sys, os
import analysis_scraping as analysissss
import locale
import analysis_scraping as analysis 
# locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

sys.path.insert(1,'../ayenda_bot_app_whatsapp/WebWhatsapp-Wrapper')
# Now do your import
from webwhatsapi import WhatsAPIDriver

class InteractionUsers:
    def __init__(self, condition_to_initialize, first_contact, last_contact, conversations, analysis_total, analysis_resume):
        self.condition_to_initialize = condition_to_initialize
        self.first_contact = first_contact
        self.last_contact = last_contact
        self.conversations = conversations
        self.analysis_total = analysis_total
        self.analysis_resume = analysis_resume
        
    def sending_messages(self):
        name_database = 'databases/henry.csv'

        if self.condition_to_initialize == 'messages':
            driver = WhatsAPIDriver('chrome', executable_path = './chromedriver')
            df = pd.read_csv(name_database)
            df = df[self.first_contact:self.last_contact]
            print(df)
            df.reset_index(inplace=True, drop=True)

            while True:
                if driver.get_status() == 'LoggedIn':
                    df.reset_index(inplace=True, drop=True)
                    print('####################################')
                    print('la cantidad de números válidos es:')
                    print(len(df))
                    print('####################################')
                    for i in range(len(df)):
                        driver.send_message_to_id(df['chat_id'][i], message=df['first_message'][i])
                        time.sleep(1)
                        print('hola')
                    self.interaction_user(driver, df)

        elif self.condition_to_initialize == 'analysis':
            driver = WhatsAPIDriver('chrome', executable_path = './chromedriver')
            df = pd.read_csv(name_database)
            df = df[self.first_contact:self.last_contact]
            df.reset_index(inplace=True, drop=True)

            while True:
                if driver.get_status() == 'LoggedIn':
                    scraping_table = analysis.whatsapp_scraping(df, driver)
                    scraping_table['contact_id'] = scraping_table.sender_id.where(~scraping_table.sender_id.isin(analysis.our_sims_ids), scraping_table.to_id)
                    respondio_hola = scraping_table.groupby('contact_id')['sender_id'].count() > 1 #si respondio 
                    respondio_hola.name = 'respondio_hola'
                    scraping_table = scraping_table.merge(respondio_hola.to_frame(), left_on='contact_id', right_on = 'contact_id')
                    scraping_table.to_csv('./scraping_analysis/' + self.conversations + '.csv')
                    # scraping_table = analysis.merged_data(analysis.info_about_app, 'info_app', scraping_table)
                    scraping_table = analysis.merged_data(analysis.error, 'error', scraping_table)
                    scraping_table = analysis.merged_data(analysis.arrive_initial_message, 'arrive_initial_message', scraping_table)

                    scraping_analysis = scraping_table.groupby('contact_id')[['respondio_hola','error', 'arrive_initial_message']].first().reset_index()
                    scraping_analysis.to_csv('./scraping_analysis/' + self.analysis_total + '.csv')
                    data = df[df['validos']==1]
                    percentages_list = [['Tipo','Cantidad', 'Contactados']]
                    percentages_list.append(analysis.percentages_analysis(scraping_analysis, 'error', True, data, 'Error'))
                    percentages_list.append(analysis.percentages_analysis(scraping_analysis, 'arrive_initial_message', 1, data, 'Llegó mensaje inicial'))
                    percentages_list.append(analysis.percentages_analysis(scraping_analysis, 'respondio_hola', True, data, 'Saludo inicial'))
                    # percentages_list.append(analysis.percentages_analysis(scraping_analysis, 'info_app', True, scraping_analysis[scraping_analysis.respondio_hola == True], 'Info App'))


                    percentages_df = pd.DataFrame(percentages_list, columns=percentages_list.pop(0))
                    print('##########################')
                    print(f'this is resume of {self.analysis_total}')
                    print(percentages_df)
                    print('##########################')
                    percentages_df.to_csv('./scraping_analysis/' + self.analysis_resume + '.csv')
                
        elif self.condition_to_initialize == 'continue messages':
            driver = WhatsAPIDriver('chrome')
            df = pd.read_csv(name_database)
            df.reset_index(inplace=True, drop=True)
            while True:
                if driver.get_status() == 'LoggedIn':
                    self.interaction_user(driver, df)

    def interaction_user(self, driver):

        stop_message = 'Es con todo el gusto del mundo, te deseo un maravilloso día 🌈'

        while True:
            all_chats = driver.get_all_chat_ids()[0:500]
            for chat in all_chats:
                messages = list(driver.get_all_messages_in_chat(chat, include_me = True))
                if len(messages) == 0:
                    continue
                if len(messages) < 3:
                    last_message = messages[-1].get_js_obj()['body']
                    user = messages[-1].get_js_obj()['sender']['id']
                    # user = str(list(user.values())[0])
                    # self.condition_to_send_messages(driver, last_message, user)
                
                if len(messages) >= 3:
                    last_message = messages[-1].get_js_obj()['body']
                    user = messages[-1].get_js_obj()['sender']['id']
                    # user = str(list(user.values())[0])
                    penultimate_message = messages[-2].get_js_obj()['body']
                    antepenultimate_message = messages[-3].get_js_obj()['body']
                    if last_message == stop_message or penultimate_message == stop_message or antepenultimate_message == stop_message:
                        continue
                    # self.condition_to_send_messages(driver, last_message, user)  
                        
    def condition_to_send_messages(self, driver, last_message, user):
        first_response_user = ['hola', 'ola', 'orden', 'servir', 'buenos', 'buenas', 'buena', 'buen', 'señora', 'bueno', 'diga', 'dígame', 'digame', 'haber', 'habe', 'pasó', 'paso', 'colaborar', 'coméntame', 'comentame', 'coménteme', 'comenteme', 'ayudarte', 'dime', 'diga', 'cuentame', 'cuéntame', 'hello', 'ayudar', 'helo', 'saludo', 'dimelo', 'dímelo', 'hole', 'ole', 'quien', 'quién', 'baby', 'babi', 'bebé', 'bebe', 'bb', 'saludito', 'perdón', 'perdon', 'sra', 'señorita', 'holaa', 'holaaa', 'holaaaa', 'hoka', 'estás', 'estas', 'bn', 'srta']
        second_response_users = ['bacano', 'gusta', 'vale', 'genial', 'super', 'bueno', 'excelente', 'interesa', 'interesado', 'interesada', 'tengo', 'descargué', 'descargue', 'uso', 'interesante', 'chevere', 'chévere', 'chebre', 'chevre', 'shevre'] 
        third_response_users = ['link', 'descargo', 'instrucciones', 'pasos', 'enviame', 'envíame', 'descargar', 'obtener', 'haré', 'hare', 'llama', 'bajo', 'aparece', 'nombre', 'play', 'ios', 'app', 'enlace']
        fourth_response_users = ['equivocada','equivocaste', 'equivocado', 'errada', 'errado', 'equivoco', 'equivocó', 'equivocados', 'errados', 'errada', 'equibocada']
        fifth_response_users = ['cuanto', 'cuánto', '%', 'porcentaje', 'descuento']
        sixth_response_users = ['tiempo', 'vence', 'caducidad', 'caduca', 'límite', 'limite', 'vigencia']
        seventh_response_users = ['tenía', 'tenia', 'instalada', 'instalé', 'ya', 'listo', 'realizado', 'hice', 'hecho', 'echo', 'hice', 'ice', 'ise', 'hise']
        eighth_response_users = ['mala', 'pésima', 'pesima', 'pecima', 'pésima','horrible', 'horrorosa', 'terrible', 'horroroza', 'orrorosa', 'orroroza']
        nineth_response_users = ['san', 'andrés']
        tenth_response_users = ['están', 'estan', 'ubicados', 'ciudades', 'hacen', 'asen', 'acen', 'hestan', 'hestán', 'presencia']
        eleventh_response_users = ['código', 'codigo', 'efectivo', 'hefectivo', 'efetivo']

        second_response = 'Hola! 😊 Soy Katherine de Ayenda hoteles, como te has hospedado en uno de nuestros hoteles queremos presentarte nuestra nueva app  https://bit.ly/newayendapp al descargarla  en las próximas 24 horas ⏳ y accedes a un 20' + '%' +' de descuento en tu primera reserva 😉, además puedes compartir el link con tus familiares y amigos para que así todos disfruten de grandes beneficios! 🤗'      
        third_response = 'Que bueno saberlo, si necesitas apoyo  con el uso del app no dudes en comentarme, para mi es un privilegio servirte 🤗'
        fourth_response = 'Claro que sí, estamos en Google Play y App Store como Ayenda Hoteles, y es muy fácil registrarte, digitas el número de celular al que te contacté y listo, puedes disfrutar de sus múltiples beneficios 😉' + '\n' + 'O también en este link puedes descargar el app https://bit.ly/newayendapp' 
        fifth_response = 'Oh comprendo, te agradezco mucho tu información y te ofrezco disculpas por la confusión 😊 un lindo día'
        sixth_response = 'Claro que sí, es del 20' + '%' + ' de descuento'
        seventh_response = 'No hay límite de tiempo para redimirlo 😉, dejamos el descuento con fecha abierta'
        eighth_response = 'Que maravilloso 🥳 ya puedes disfrutar de sus beneficios, recuerda que siempre el mejor precio lo tendremos en el app de nuestros 480 hoteles'
        nineth_response = 'Comprendo al máximo , estamos trabajando para mejorar nuestra falencias, te ofrecemos mil disculpas por la situación incómoda que viviste, lo hablaremos con el área encargada, infinitas gracias por tu valioso aporte 🤗'
        tenth_response = 'Aún no hacemos presencia en San Andrés Islas'
        eleventh_response = 'Hacemos presencia en  Medellín, Bogotá, Soacha, Tunja, Puerto Colombia, Pereira, Barranquilla, Cali, Rionegro, Palmira, Soledad, Chía, Valledupar, Riohacha Armenia, Ibagué, Manizales, Villavicencio, Bucaramanga, Santa Marta, Cúcuta, Cartagena, Soacha, Malambo, Neiva, Montería y Lima , Arequipa, Trujillo, Piura, Cusco, Chiclayo, Ica - Perú , Ciudad de México y Guadalajara'
        twelveth_response = 'Claro que si, es muy simple 😊 buscas la fecha que necesitas para viajar, escoges un Ayenda ideal  para ti y listo, cuando le des aceptar a la reserva, el sistema automáticamente te aplica el descuento y puedes visualizar la diferencia de la tarifaria 😉'

        our_sims_ids = ['573054158965@c.us', '573053032694@c.us', '573244755031@c.us', '573244755013@c.us', '573013209450@c.us', '573052527680@c.us', '573004669489@c.us', '573225168965@c.us', '573126055649@c.us', '573235351019@c.us']

        if (type(last_message) == str) and (user not in our_sims_ids):
            last_message = last_message.lower().split()
            for i in range(len(last_message)):
                last_message[i] = last_message[i].replace(' ', '')
                last_message[i] = last_message[i].replace(',', '')
                last_message[i] = last_message[i].replace('.', '')
                last_message[i] = last_message[i].replace(';', '')
                last_message[i] = last_message[i].replace('?', '')
                last_message[i] = last_message[i].replace('¿', '')
                last_message[i] = last_message[i].replace('!', '')
                last_message[i] = last_message[i].replace('¡', '')
            if any([word in last_message for word in first_response_user]):
                driver.send_message_to_id(user, message = second_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in second_response_users]):
                driver.send_message_to_id(user, message = third_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in third_response_users]):
                driver.send_message_to_id(user, message = fourth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in fourth_response_users]):
                driver.send_message_to_id(user, message = fifth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in fifth_response_users]):
                driver.send_message_to_id(user, message = sixth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in sixth_response_users]):
                driver.send_message_to_id(user, message = seventh_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in seventh_response_users]):
                driver.send_message_to_id(user, message = eighth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in eighth_response_users]):
                driver.send_message_to_id(user, message = nineth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in nineth_response_users]):
                driver.send_message_to_id(user, message = tenth_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in tenth_response_users]):
                driver.send_message_to_id(user, message = eleventh_response)
                driver.chat_send_seen(user)
            if any([word in last_message for word in eleventh_response_users]):
                driver.send_message_to_id(user, message = twelveth_response)
                driver.chat_send_seen(user)