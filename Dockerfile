FROM python:3.11-rc-slim

RUN apt update && mkdir /fusionstyle

WORKDIR /fusionstyle

COPY ./src ./src ./\
    ./requirements.txt ./requirements.txt ./\
    ./commands ./commands ./


RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

CMD ["bash"]