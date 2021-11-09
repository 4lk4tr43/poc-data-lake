FROM node:alpine

RUN apk add g++ make python3
RUN npm install node-gyp -g

WORKDIR /app

ADD package.json /app
ADD package-lock.json /app
RUN npm i

ADD ./ /app

ENTRYPOINT npm run dev
