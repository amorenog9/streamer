FROM python:3.8
WORKDIR /app

RUN apt-get update 
RUN apt-get upgrade -y 


# Clonar repositorio
RUN	git clone https://github.com/amorenog9/streamingProject.git

# Creacion de jar
WORKDIR /app/streamingProject
RUN sbt clean
RUN sbt assembly
WORKDIR /app/streamingProject/target/scala-2.11
RUN chmod 777 streamingProject-assembly-0.1.jar



