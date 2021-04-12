FROM amsterdam/python:3.8-slim-buster-minimal
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
COPY uwsgi.ini /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY authstatus /app/authstatus
COPY tests /app/tests
COPY docker-entrypoint.sh /app/
COPY docker-test.sh /app/

CMD ["/app/docker-entrypoint.sh"]
