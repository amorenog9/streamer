from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return "Pagina Inicio del servidor en kafka"
    
@app.route("/pwd")
def pwd():
    return subprocess.check_output(["pwd"])

@app.route("/topics")
def topics():
    try:
        output = subprocess.check_output(["/app/kafka_2.12-3.0.0/bin/kafka-topics.sh", "--bootstrap-server", "localhost:9092", "--list"])
        return output
    except subprocess.CalledProcessError as e:
        return "Error al obtener la lista de topics: {}".format(e)
    
@app.route("/create/<topic_name>")
def create(topic_name):
    try:
        output = subprocess.check_output(["/app/kafka_2.12-3.0.0/bin/kafka-topics.sh", "--create", "--bootstrap-server", "localhost:9092", "--replication-factor", "1", "--partitions", "1", "--topic", topic_name])
        return "Topic creado: {}".format(topic_name)
    except subprocess.CalledProcessError as e:
        return "Error al crear el topic: {}".format(e)

    
@app.route("/delete/<topic_name>")
def delete(topic_name):
    try:
        output = subprocess.check_output(["/app/kafka_2.12-3.0.0/bin/kafka-topics.sh", "--bootstrap-server", "localhost:9092", "--delete", "--topic", topic_name])
        return "Topic eliminado: {}".format(topic_name)
    except subprocess.CalledProcessError as e:
        return "Error al eliminar el topic: {}".format(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)

