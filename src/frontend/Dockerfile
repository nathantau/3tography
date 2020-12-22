FROM node:alpine

RUN mkdir -p /home/frontend
WORKDIR /home/frontend

COPY package.json /home/frontend
# COPY package-lock.json /home/frontend

RUN npm config set registry http://registry.npmjs.org/
RUN npm install

COPY . /home/frontend

CMD ["npm", "run", "start"]
