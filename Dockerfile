FROM python:3.8.5-alpine
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip 
WORKDIR /app
ADD . /app
RUN pip --no-cache-dir install -r requirements.txt
CMD ["python","app.py"]