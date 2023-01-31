from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import pyspark
from delta import *
from time import sleep


KAFKA_TOPIC_IN = "messages_out_no_memory"  # Stream infinito
KAFKA_TOPIC_OUT = 'messages_from_timestamp_out'
broker = "localhost:9092"

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(3, 0, 0))


builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Obtengo de una tabla parametros que necesite de scala (timestamp y ruta del fichero)
df = spark.read.format("delta").load("/tmp/events_from_timestamp/delta-table")  # Esta tabla se actualizara cada vez que ejecutemos SparkReaderTable.scala
df.show()

actualTime = df.first()['actualTime']
routeToFile = df.first()['routeToFile']



# Primero enviamos al kafkaTopic los mensajes del fichero eventsFromTimestamo y luego enviamos desde el punto donde lo dejamos el stream infinito (messages_out)
# Creamos un stream finito con los valores de la tabla hasta el momento
def getAndProduceMessagesFromFile(file_path, topic_out):
    # Using readlines()
    file1 = open(file_path, 'r')
    Lines = file1.readlines()

    for line in Lines:
        print(line.rstrip('\n'))
        producer.send(topic_out,line.rstrip('\n').encode())  # debemos enviar como byte[] a flink para que JsonNodeDeserializationSchema() pueda leerlo
        producer.flush()


getAndProduceMessagesFromFile(routeToFile + "/eventsFromTimestamp.json", KAFKA_TOPIC_OUT)


# Concatenamos el stream infinito debajo de los eventos de la tabla finita
def getAndProduceMessagesFromTimestamp(timestamp, topic_in, topic_out):
    consumer = KafkaConsumer(topic_in, bootstrap_servers=broker, enable_auto_commit=True)
    consumer.poll()  # we need to read message or call dumb poll before seeking the right position

    tp = TopicPartition(topic_in, 0)  # partition n. 0

    rec_in = consumer.offsets_for_times({tp: timestamp})
    consumer.seek(tp, rec_in[tp].offset)


    for msg in consumer:
        print(msg.value.decode())
        producer.send(topic_out, msg.value.decode().encode())
        producer.flush()


getAndProduceMessagesFromTimestamp(actualTime, KAFKA_TOPIC_IN, KAFKA_TOPIC_OUT)
