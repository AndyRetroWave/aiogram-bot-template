FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv

RUN pip install --upgrade pip \
        && pip install -r requirements.txt \
        && rm -rf requirements

COPY . .

CMD ["python", "./bot.py"]
