FROM python:3.10

ENV PYTHONUNBUFFERED=1

#ENV INSTANCE=
#ENV DISTRICT=
#ENV SCHOOL=
#ENV MENU=
#ENV mongo_ip=
#ENV mongo_port=
#ENV webdriver_address=

RUN apt update

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./ /app
WORKDIR /app

CMD ["python3", "main.py"]
