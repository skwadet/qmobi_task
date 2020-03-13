FROM python:3.8.0
LABEL maintainer="skwadet@protonmail.com"
VOLUME ["/qmobi_task"]
COPY . /qmobi_task
WORKDIR /qmobi_task
CMD ["python3", "http_server.py", "172.17.0.2", "8000"]
