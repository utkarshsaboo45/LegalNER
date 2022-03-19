FROM python:3.8-slim-buster

WORKDIR "/interface"

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "backend.py"]