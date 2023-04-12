FROM node:18.14.0

WORKDIR /app

# Clonar repositorio
RUN	git clone https://github.com/amorenog9/eventsdashboard.git

# Trabajar en la carpeta 
WORKDIR /app/eventsdashboard

# Instalacion de dependencias
RUN npm install

# Iniciamos cluster flink y ejecutamos Job
CMD node server.js




