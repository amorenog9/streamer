FROM openjdk:8

WORKDIR /app

# Spark
RUN wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz 
RUN tar -xzvf spark-2.4.8-bin-hadoop2.7.tgz


WORKDIR /app/spark-2.4.8-bin-hadoop2.7/conf

COPY spark-env.sh .

RUN chmod 777 spark-env.sh

WORKDIR /app/spark-2.4.8-bin-hadoop2.7/conf/sbin

COPY script.sh .

RUN chmod 777 script.sh

CMD ./script.sh













