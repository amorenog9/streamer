import binascii
import json
from datetime import datetime
from kafka import KafkaProducer

from time import sleep
import pandas as pd

KAFKA_TOPIC = 'messages_in'

producer = KafkaProducer(bootstrap_servers=['localhost:9093'], api_version=(3, 0, 0))

def generator(data):
    for i in range(len(data)):
        sleep(0.1)  #sleep(deltas[i])
        yield data.iloc[i].to_json()+"\n"  #Por defecto on date_format = 'epoch' -> 1484856900000 (epoch milliseconds)

if __name__ == '__main__':
    g = generator(pd.read_feather("../data/anubisShorted_shortedSimple_3columns.feather"))
    for line in g:
        print(line)
        producer.send(KAFKA_TOPIC, line.encode()) #debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
        # block until all async messages are sent
        producer.flush()
    while True:
        sleep(1)  # Para que no termine nunca de enviar mensajes y el fichero SparkReaderTable funcione correctamente


        

