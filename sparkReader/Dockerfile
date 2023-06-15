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

# Instalacion de wget, curl y sudo
RUN apt-get update && apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install sudo -y


# Pasos necesarios para instalar servidor flask
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5006


# SBT - instalacion
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" |  tee /etc/apt/sources.list.d/sbt.list
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" |  tee /etc/apt/sources.list.d/sbt_old.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" |  apt-key add
RUN apt-get update
RUN apt-get install -y sbt

# Obtener spark
RUN wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz 
RUN tar -xzvf spark-2.4.8-bin-hadoop2.7.tgz

#COPY . .

# Clonar repositorio
RUN	git clone https://github.com/amorenog9/streamingProject.git

# Creacion de jar
WORKDIR /app/streamingProject
RUN sbt clean
RUN sbt assembly
WORKDIR /app/streamingProject/target/scala-2.11
RUN chmod 777 streamingProject-assembly-0.1.jar


WORKDIR /app
CMD python3 app_cluster_spark.py



