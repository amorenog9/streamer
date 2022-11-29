import binascii
import json
from datetime import datetime
from kafka import KafkaProducer

from time import sleep
import pandas as pd

KAFKA_TOPIC = 'messages_in'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def generator(data):
   # deltas = data.delta.values
   # data_rows = data.drop(columns=["delta"])
    for i in range(len(data)):
        sleep(0.2) #sleep(deltas[i])
        yield data.iloc[i].to_json()+"\n" #Por defecto on date_format = 'epoch' -> 1484856900000 (epoch milliseconds)
        #yield data.iloc[i].to_json(date_format='iso')+"\n" #Con date_format = 'iso' -> "2017-01-19T20:15:00.000"
        #yield data_rows.iloc[i].to_json()+"\n"

if __name__ == '__main__':
    g = generator(pd.read_feather("../data/anubisShorted_shortedSimple_3columns.feather"))
    for line in g:
        #print(f'Producing message @ {datetime.now()} | Message = {str(line)}')
        print(line)
        producer.send(KAFKA_TOPIC, line.encode()) #debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
        # block until all async messages are sent
        producer.flush()


        

