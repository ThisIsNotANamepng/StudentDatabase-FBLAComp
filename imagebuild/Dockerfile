FROM docker.io/python:3.12.0b3-slim-bullseye

RUN pip3 install flask

RUN apt update

RUN apt upgrade -y

RUN apt install git -y

RUN git clone https://github.com/ThisIsNotANamepng/buythcgfhvgchc.git fbla

RUN apt install rsync -y

WORKDIR /

RUN alias

RUN echo "alias involve-start='python3 /fbla/startserver.py'" >> ~/.bashrc
RUN echo "alias involve-stop='python3 /fbla/stopserver.py'" >> ~/.bashrc
RUN echo "alias involve-diagnostics='python3 /fbla/diagnostics.py'" >> ~/.bashrc

ENTRYPOINT ["python3", "/fbla/startserver.py"]
