FROM python:3.8
WORKDIR /app

RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install sudo -y


# Clonar repositorio
RUN git clone https://github.com/amorenog9/streamer.git

# Ejecucion de servidor flask
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5005
CMD ["python", "app.py"]





