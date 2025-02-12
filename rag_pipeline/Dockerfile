FROM apache/airflow:2.10.4

RUN pip install --upgrade pip

RUN apt update && apt install -y awscli

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
