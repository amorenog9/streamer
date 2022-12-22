from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import os
import time

KAFKA_TOPIC_OUT = 'messages_from_timestamp'
broker = "localhost:9092"

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 0, 0))


##########################################################
# Cojo de una tabla y leo los parametros que necesite :)
##########################################################

def getAndProduceMessagesFromFile(file_path, topic_out):
    # Using readlines()
    file1 = open(file_path, 'r')
    Lines = file1.readlines()

    for line in Lines:
        print(line)
        producer.send(topic_out, line.encode())  # debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
        producer.flush()


#getAndProduceMessagesFromFile("/tmp/events_from_timestamp/1/eventsFromTimestamp.json", KAFKA_TOPIC_OUT)


def getAndProduceMessagesFromTimestap(timestamp, topic_in, topic_out):
    consumer = KafkaConsumer(topic_in, bootstrap_servers=broker, enable_auto_commit=True)
    consumer.poll()  # we need to read message or call dumb poll before seeking the right position

    tp = TopicPartition(topic_in, 0)  # partition n. 0

    # in fact you asked about how to use 2 methods: offsets_for_times() and seek()
    rec_in = consumer.offsets_for_times({tp: timestamp})
    consumer.seek(tp, rec_in[tp].offset)  # lets go to the first message in New Year!

    for msg in consumer:
        print(msg.value.decode())
        producer.send(topic_out, msg.value.decode().encode())
        producer.flush()


getAndProduceMessagesFromTimestap(1671705669287, "messages_out", KAFKA_TOPIC_OUT)
