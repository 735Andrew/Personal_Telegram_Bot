FROM python:3.12.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y  git && \
    apt-get install -y postgresql-client && \
    apt-get install -y libpq-dev && \
    apt-get install -y gcc && \
    apt-get clean

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app /app/app
COPY project.py /app/project.py
COPY config.py /app/config.py

EXPOSE 8000
CMD ["python", "project.py"]