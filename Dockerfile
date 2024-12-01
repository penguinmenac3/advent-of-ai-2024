FROM python:3.12-alpine

RUN apk update && apk upgrade
RUN apk add git openssh make g++ curl

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

WORKDIR /workspaces/adventofcode-2024

# For deployment use this
#RUN npm i -g serve
#COPY . .
#RUN npm run build
#EXPOSE 3000

#CMD [ "serve", "-s", "dist" ]
