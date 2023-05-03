FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt install -y python3-dev python3-pip python3-venv git curl && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]