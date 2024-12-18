FROM python:3.12-bookworm

RUN apt update && apt upgrade
RUN apt install -y git openssh-client g++ curl build-essential golang

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN pip install bs4 requests tqdm

WORKDIR /workspaces/adventofcode-2024

# For deployment use this
#RUN npm i -g serve
#COPY . .
#RUN npm run build
#EXPOSE 3000

#CMD [ "serve", "-s", "dist" ]
