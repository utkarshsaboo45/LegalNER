FROM python:3.8-slim-buster

WORKDIR "/Users/snehajhaveri/Documents/Legal_App"

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "backend.py"]