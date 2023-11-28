# syntax=docker/dockerfile:1.2
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

EXPOSE 80

COPY ./challenge /code/challenge

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "80"]