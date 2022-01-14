FROM ubuntu:18.04
COPY . /app
RUN apt update && apt install python3-pip mysql-client curl locales locales-all prometheus-node-exporter -y
RUN pip3 install requests Flask pymysql flask-mysql prometheus-flask-exporter
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
CMD  FLASK_APP=/app/main.py flask run -h 0.0.0.0
EXPOSE 5000/tcp 
EXPOSE 9100/tcp
