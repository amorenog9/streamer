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

@app.route("/script")
def script():
    print("Ejecutamos el script TemporalStreamProducer.py")
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    try:
        output = subprocess.check_output(["python3", "/app/streamer/kafka/TemporalStreamProducer.py"])
        return output
    except subprocess.CalledProcessError as e:
        return "Error al ejecutar el script: {}".format(e)


@app.route("/script2")
def script2():
    try:
        output = subprocess.check_output(["python3", "/app/test.py"])
        return output
    except subprocess.CalledProcessError as e:
        return "Error al ejecutar el script: {}".format(e)


@app.route("/kill/<temporal_process>")
def kill(temporal_process):
    print("TemporalProcess eliminado:", temporal_process)
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    try:
        output = subprocess.check_output(["sudo", "pkill", "-f", temporal_process])
        return "Proceso temporal eliminado"
    except subprocess.CalledProcessError as e:
        return "Error al eliminar el proceso temporal: {}".format(e)
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)

