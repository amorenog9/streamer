import json
from kafka import KafkaConsumer
KAFKA_TOPIC = 'messages_out_no_memory'
#KAFKA_TOPIC = 'messages_out'
#KAFKA_TOPIC = 'messages_in'

if __name__ == '__main__':
    # Kafka Consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        #auto_offset_reset='latest',
        api_version=(3, 0, 0)

    )
    for message in consumer:
        print(message)
        #print(message.value.decode())
        #print(message.timestamp)
