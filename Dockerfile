FROM python:3-alpine
WORKDIR /app
RUN apk --no-cache add gcc musl-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
CMD ["python", "./app/hycord.py"]
