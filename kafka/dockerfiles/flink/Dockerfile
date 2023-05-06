FROM openjdk:8

WORKDIR /app

# SBT - instalacion
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" |  tee /etc/apt/sources.list.d/sbt.list
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" |  tee /etc/apt/sources.list.d/sbt_old.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" |  apt-key add
RUN apt-get update
RUN apt-get install sbt


# Flink en /app


# Descargamos flink en /app
#RUN  wget https://archive.apache.org/dist/flink/flink-1.12.1/flink-1.12.1-bin-scala_2.11.tgz
#RUN tar -xvzf flink-1.12.1-bin-scala_2.11.tgz

COPY . .

# Clonar repositorio
RUN	git clone https://github.com/amorenog9/streamingProject.git

# Creacion de jar
WORKDIR /app/streamingProject
RUN sbt clean
RUN sbt assembly
WORKDIR /app/streamingProject/target/scala-2.11
RUN chmod 777 streamingProject-assembly-0.1.jar

# Trabajar dentro del repositorio de flink
WORKDIR /app/flink-1.12.1/bin

# Iniciamos cluster flink y ejecutamos Job
CMD ./start-cluster.sh -Drest.port=7080 && ./flink run -c es.upm.dit.Job ../../streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar 



