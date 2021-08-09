FROM python:3.8

RUN mkdir app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN rm requirements.txt

COPY manage.py .

COPY boilerplate/ boilerplate

ENV CURL_CA_BUNDLE=""

EXPOSE 5000

CMD ["python3", "-u", "manage.py"]
