FROM python:3.10-slim

ENV PORT 8080

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python3", "heicconverter.py"]