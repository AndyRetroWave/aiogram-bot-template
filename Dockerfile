FROM python:3.10-slim

RUN mkdir /contora

WORKDIR /contora

COPY requirements.txt .

RUN python -m venv venv

RUN pip install -r requirements.txt 

COPY . .

CMD ["python", "./bot.py"]