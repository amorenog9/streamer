from flask import Flask
import subprocess
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "Pagina Inicio del servidor de python"
    
@app.route("/pwd")
def pwd():
    return subprocess.check_output(["pwd"])

@app.route("/spark-submit/<resultDay>/<resultDate>/<listIds>")
def submit(resultDay, resultDate, listIds):
    print("resultDay:", resultDay, "resultDate:", resultDate, "listIds:", listIds)
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    resultDate = resultDate.replace("-", "/") #cambiamos a / de nuevo
    print("resultDay:", resultDay, "resultDate:", resultDate, "listIds:", listIds)
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    try:
        output = subprocess.check_output(["/app/spark-2.4.8-bin-hadoop2.7/bin/spark-submit", "--class", "es.upm.dit.SparkReaderTable", "--master", "local[*]", "--jars", "/app/streamingProject/bibliotecas_jars/delta-core_2.11-0.6.1.jar", "/app/streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar", resultDay, resultDate, listIds])
        return "Spark-submit enviado al servidor con parametros {}, {}, {}".format(resultDay, resultDate, listIds)
    except subprocess.CalledProcessError as e:
        return "Error al ejecutar el jar spark submit: {}".format(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006)


