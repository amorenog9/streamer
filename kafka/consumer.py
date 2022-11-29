import json 
from kafka import KafkaConsumer

if __name__ == '__main__':
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'messages_out',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        print(message.value.decode())
