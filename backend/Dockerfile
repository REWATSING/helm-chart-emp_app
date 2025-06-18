FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip list

COPY . . 

CMD [ "python3", "app.py" ]