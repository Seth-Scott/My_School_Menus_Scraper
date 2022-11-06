FROM python:3.10
# docker run -d --env-file .env.container -v /etc/localtime:/etc/localtime <docker_image>
RUN apt update

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./ /app
WORKDIR /app

CMD ["python3", "main.py"]
