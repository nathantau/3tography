# FROM node:alpine

# RUN mkdir -p /home/frontend
# WORKDIR /home/frontend

# COPY package /home/frontend

# RUN npm config set registry http://registry.npmjs.org/
# # RUN npm install -g react-scripts
# RUN npm install

# COPY . /home/frontend

# CMD ["npm", "run", "start"]

FROM node:alpine

WORKDIR /app

COPY package.json /app

RUN yarn install

COPY . /app

CMD ["yarn", "run", "start"]