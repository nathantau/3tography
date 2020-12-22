FROM node:alpine

RUN mkdir -p /home/backend
WORKDIR /home/backend

COPY package-lock.json /home/backend

RUN npm config set registry http://registry.npmjs.org/
RUN npm install

COPY . /home/backend

CMD ["node", "app.js"]
