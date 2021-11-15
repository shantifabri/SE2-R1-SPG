FROM python:3
RUN apt-get update
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install pysqlite3
WORKDIR /app
COPY . /app
RUN pip3 install --requirement /app/requirements.txt
EXPOSE 5000
CMD [ "python", "./app.py"]