from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json

from time import sleep

KAFKA_TOPIC_IN = "messages_out_no_memory"  # Stream infinito
KAFKA_TOPIC_OUT = 'messages_from_timestamp_out'


# Configuración de Kafka
bootstrap_servers = 'localhost:9092'
auto_offset_reset = 'earliest'
enable_auto_commit = True
group_id = 'my-group'
value_deserializer = lambda m: json.loads(m.decode('utf-8'))

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 0, 0))

# Abrimos JSON
f = open('/tmp/events_from_timestamp/variables_python/variables.json')
data = json.load(f)

# Almacenamos variables
actualTime = data['actualTime']
routeToFile = data['routeToFile']

# Cerramos JSON
f.close()

print(actualTime)
print(routeToFile)


# Primero enviamos al kafkaTopic los mensajes del fichero eventsFromTimestamo y luego enviamos desde el punto donde lo dejamos el stream infinito (messages_out)
# Creamos un stream finito con los valores de la tabla hasta el momento
def getAndProduceMessagesFromFile(file_path, topic_out):
    # Using readlines()
    file1 = open(file_path, 'r')
    Lines = file1.readlines()

    for line in Lines:
        # print(line.rstrip('\n'))
        producer.send(topic_out, line.rstrip(
            '\n').encode())  # debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
        producer.flush()


getAndProduceMessagesFromFile(routeToFile + "/eventsFromTimestamp.json", KAFKA_TOPIC_OUT)


# Concatenamos el stream infinito debajo de los eventos de la tabla finita
def getAndProduceMessagesFromTimestamp(timestamp, topic_in, topic_out):

    # Crear objeto KafkaConsumer
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=enable_auto_commit,
        group_id=group_id,
        value_deserializer=value_deserializer
    )

    # Obtener el timestamp deseado
    timestamp_ms = timestamp

    # Buscar el offset del primer mensaje en el topic
    tp = TopicPartition(topic_in, 0)
    consumer.assign([tp])
    consumer.seek_to_beginning(tp)

    # Consumir mensajes hasta encontrar el mensaje deseado
    for message in consumer:
        if message.timestamp >= timestamp_ms:
            print(message)
            message_json = json.dumps(message.value) # convert dict to JSON string
            producer.send(topic_out, value=message_json.encode('utf-8'))
            producer.flush()


getAndProduceMessagesFromTimestamp(actualTime, KAFKA_TOPIC_IN, KAFKA_TOPIC_OUT)