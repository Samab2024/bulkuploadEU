FROM python:2.7
COPY . /app
CMD [ "python", "/app/bulkupload.py" ]