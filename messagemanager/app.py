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

@app.route("/produceTrains")
def script():
    print("Ejecutamos el script producer.py")
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    try:
        output = subprocess.check_output(["python3", "producer.py"])
        return output
    except subprocess.CalledProcessError as e:
        return "Error al ejecutar el script: {}".format(e)
        
@app.route("/produceTrucks")
def script2():
    print("Ejecutamos el script producer_trucks.py")
    sys.stdout.flush() # vaciar la salida a la consola del servidor
    try:
        output = subprocess.check_output(["python3", "producer_trucks.py"])
        return output
    except subprocess.CalledProcessError as e:
        return "Error al ejecutar el script: {}".format(e)        

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007)

