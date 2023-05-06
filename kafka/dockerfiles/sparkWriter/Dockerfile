FROM openjdk:8

WORKDIR /app

# SBT - instalacion
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" |  tee /etc/apt/sources.list.d/sbt.list
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" |  tee /etc/apt/sources.list.d/sbt_old.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" |  apt-key add
RUN apt-get update
RUN apt-get install sbt


RUN apt-get install sudo -y


# Obtener spark
#RUN wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz 
#RUN tar -xzvf spark-2.4.8-bin-hadoop2.7.tgz
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
WORKDIR /app/spark-2.4.8-bin-hadoop2.7/bin

# Enviamos job a spark, esperamos 60 segundos para dar margen a los workers a que se creen (podría no ser necesario, pero no está de más), le damos solo 1 core

#CMD ./spark-submit --class es.upm.dit.KafkaSparkWriter --master local[*] --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.8 --jars /app/streamingProject/bibliotecas_jars/delta-core_2.11-0.6.1.jar /app/streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar 

CMD sleep 60 && ./spark-submit --total-executor-cores $NUMBER_CORES --class es.upm.dit.KafkaSparkWriter --master spark://$SPARK_HOST:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.8 --jars /app/streamingProject/bibliotecas_jars/delta-core_2.11-0.6.1.jar /app/streamingProject/target/scala-2.11/streamingProject-assembly-0.1.jar 

