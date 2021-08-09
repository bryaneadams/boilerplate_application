FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN rm requirements.txt

COPY . /home

WORKDIR /home

CMD ["python", "boiler_worker.py"]