FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install iputils-ping -y
RUN mkdir /home/lab2
RUN cd /home/lab2
COPY ./mtu.py /home/lab2/mtu.py
ENTRYPOINT ["python3", "/home/lab2/mtu.py"]
