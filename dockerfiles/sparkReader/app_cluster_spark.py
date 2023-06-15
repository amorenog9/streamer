from flask import Flask
import subprocess
import sys

app = Flask(__name__)

# Ruta para la página de inicio
@app.route("/")
def index():
    return "Pagina Inicio del servidor de python"
    
# Ruta para obtener el directorio actual
@app.route("/pwd")
def pwd():
    return subprocess.check_output(["pwd"])

# Ruta para enviar un spark-submit al servidor
@app.route("/spark-submit/<resultDay>/<resultDate>/<listIds>")
def submit(resultDay, resultDate, listIds):
    print("resultDay:", resultDay, "resultDate:", resultDate, "listIds:", listIds)
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    resultDate = resultDate.replace("-", "/")
    print("resultDay:", resultDay, "resultDate:", resultDate, "listIds:", listIds)
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    
    try:
        # Comando para matar cualquier proceso que tenga el nombre "SparkReaderTable" y luego enviar un spark-submit al servidor
        command = "pgrep -f SparkReaderTable | xargs kill -9 ; /app/spark-2.4.8-bin-hadoop2.7/bin/spark-submit --total-executor-cores 3 --class es.upm.dit.SparkReaderTable --master spark://spark:7077 --jars /app/streamingProject/bibliotecas_jars/delta-core_2.11-0.6.1.jar /app/streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar {} {} {}".format(resultDay, resultDate, listIds)
        output = subprocess.check_output(command, shell=True)
        return "Spark-submit enviado al servidor con parametros {}, {}, {}".format(resultDay, resultDate, listIds)
    
    except subprocess.CalledProcessError as e:
        # En caso de error, intenta enviar el spark-submit nuevamente sin matar ningún proceso previamente
        command2 = "/app/spark-2.4.8-bin-hadoop2.7/bin/spark-submit --total-executor-cores 3 --class es.upm.dit.SparkReaderTable --master spark://spark:7077 --jars /app/streamingProject/bibliotecas_jars/delta-core_2.11-0.6.1.jar /app/streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar {} {} {}".format(resultDay, resultDate, listIds)
        return subprocess.check_output(command2, shell=True)

if __name__ == "__main__":
    # Inicia el servidor en el puerto 5006 y en todas las direcciones
    app.run(host='0.0.0.0', port=5006)

