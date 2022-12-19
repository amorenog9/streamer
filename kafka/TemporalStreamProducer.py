
from kafka import KafkaProducer
import os

KAFKA_TOPIC = 'messages_timestamp_query'

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 0, 0))


# Look for your absolute directory path
absolute_path = os.path.dirname(os.path.abspath(__file__))

file_path = "/tmp/events_from_timestamp/2/eventsFromTimestamp.json"


# Using readlines()
file1 = open(file_path, 'r')
Lines = file1.readlines()

for line in Lines:
    print(line)
    producer.send(KAFKA_TOPIC, line.encode()) #debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
    producer.flush()




        

