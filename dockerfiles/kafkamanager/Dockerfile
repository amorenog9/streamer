FROM ubuntu:20.04

# Instalacion de python y jdk8-java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN apt-get update -y \
&& apt-get install -y software-properties-common \
&& add-apt-repository ppa:deadsnakes/ppa \
&& apt-get install openjdk-8-jdk -y \
&& apt-get install python3-pip -y \
&& export JAVA_HOME \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Instalacion de wget y curl
RUN apt-get update && apt-get install -y wget
RUN apt-get install -y curl

# Pasos necesarios para instalar servidor flask
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5008


# Instalacion de zookeeper y kafka en docker
WORKDIR /app

COPY . .

RUN mv start-topics.sh /app/kafka_2.12-3.0.0

#Ejecucion de kafka y servidor flask
WORKDIR /app/kafka_2.12-3.0.0

RUN ls -ll

RUN chmod +x ./start-topics.sh

CMD ./start-topics.sh && python3 ../app.py







