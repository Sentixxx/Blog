FROM python:3.11

WORKDIR /backend

COPY . /backend


RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 8090

CMD ["python","manage.py"]

