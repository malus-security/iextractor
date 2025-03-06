FROM debian:latest

RUN apt update && apt upgrade -y

RUN apt install -y git build-essential

RUN git clone https://github.com/malus-security/iextractor.git

WORKDIR /iextractor/tools/lzssdec

RUN make

ENTRYPOINT [ "/iextractor/tools/lzssdec/lzssdec" ]
