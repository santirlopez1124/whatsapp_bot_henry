from sshtunnel import SSHTunnelForwarder
import pandas as pd
import psycopg2

def quotation(checkin, checkout, hotel, room_type, paxes):
    # Create an SSH tunnel
    tunnel = SSHTunnelForwarder(
        ('10.8.0.18', 1002),
        ssh_username='replicator',
        ssh_private_key='id_rsa',
        remote_bind_address=('localhost', 10287),
        local_bind_address=('0.0.0.0',10291), # could be any available port
    )
    tunnel.stop()
    tunnel.start()

    conn = psycopg2.connect(
        database='ayenda_production',
        user='srojas',
        host=tunnel.local_bind_host,
        port=tunnel.local_bind_port,
        password='9d26c01f69ccb3a9c4acefdeb4f54344'
    )

    last_front_otas_users = f'''SELECT DISTINCT 
--room_type_rates.id, 
room_type_rates.date, 
--room_type_rates.room_type_id, 
room_type_rates.pax, 
room_type_rates.value,
--room_type_rates.last_value, 
--room_type_rates.with_variable_rates, 
--room_type_rates.kind, 
--room_type_rates.is_edited, 
--room_type_rates.promotion_value, 
--room_type_rates.rate_increase_value, 
--oom_type_rates.variation_rates
h.name_without_accents as hotel
FROM room_type_rates
join room_types rt on rt.id = room_type_rates.room_type_id
join hotels h on h.id = rt.hotel_id
WHERE room_type_rates.date BETWEEN '{checkin}' AND date '{checkout}'
AND room_type_rates.id IN (SELECT MAX(room_type_rates.id) 
                            FROM room_type_rates
                            join room_types rt2 on rt2.id = room_type_rates.room_type_id
                            join hotels h on h.id = rt2.hotel_id 
                            WHERE room_type_rates.date  BETWEEN '{checkin}' AND  date '{checkout}'::date - 1 
                            AND  rt2.name_without_accents like '%{room_type}%'
                            and h.name_without_accents like '%{hotel}%'
                            AND room_type_rates.kind = 3
                            GROUP BY room_type_id, date, kind, pax)
and room_type_rates.pax = {paxes}
                            '''

    user_quotations = pd.read_sql_query(last_front_otas_users, conn)
    # tunnel.stop()
    return user_quotations


        