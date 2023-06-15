FROM openjdk:8-jdk

# Descargar Spark
WORKDIR /main

# Obtener spark
RUN wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz 
RUN tar -xzvf spark-2.4.8-bin-hadoop2.7.tgz

# Configramos parametros spark 
WORKDIR /main/spark-2.4.8-bin-hadoop2.7/conf

RUN ls -ll
RUN rm -r spark-env.sh.template
RUN rm -r spark-defaults.conf.template
COPY spark-env.sh .
COPY spark-defaults.conf .
RUN chmod 777 spark-env.sh
RUN chmod 777 spark-defaults.conf

# Iniciamos master y 1 worker
WORKDIR /main/spark-2.4.8-bin-hadoop2.7/sbin

CMD ./start-master.sh & ./start-slave.sh spark://$SPARK_HOST:7077 & sleep infinity





