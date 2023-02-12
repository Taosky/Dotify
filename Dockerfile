FROM python:3.7-alpine

WORKDIR /app
ADD . /app

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip && \
 pip install --no-cache-dir -r requirements.txt

EXPOSE 4023
ENTRYPOINT ["/app/entrypoint.sh"] 
 