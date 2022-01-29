FROM python:3.10-buster

ENV PORT 8080

COPY . .
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python3", "heicconverter.py"]