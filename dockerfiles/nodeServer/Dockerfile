FROM node:18.14.0

EXPOSE 3001

WORKDIR /app

# Clonar repositorio
RUN	git clone https://github.com/amorenog9/eventsdashboard.git

# Trabajar en la carpeta 
WORKDIR /app/eventsdashboard

# Instalacion de dependencias
RUN npm install

# Esperamos 10segundos para que los topics esten creados e iniciamos el servidor
CMD sleep 30 && node server.js




