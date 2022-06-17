FROM ubuntu:kinetic-20220602

LABEL maintainer="gulbinowicz.piotr@gmail.com"

RUN apt update \
 && apt install procps=2:3.3.17-6ubuntu2 -y \
 && apt install python3=3.10.4-0ubuntu2 -y \
 && apt install uvicorn=0.15.0-2ubuntu1 -y \
 && apt install python3-pip=22.1.1+dfsg-1 -y

RUN pip3 install fastapi==0.78.0 \
&& pip3 install redis==4.3.3

ADD main.py /root

EXPOSE 8000

CMD cd /root && uvicorn main:app --host 0.0.0.0 --port 8000
