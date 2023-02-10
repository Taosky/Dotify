FROM python:3.7-slim

WORKDIR /app
ADD . /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 4023
ENTRYPOINT ["/app/entrypoint.sh"] 
 