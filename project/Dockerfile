FROM ubuntu
RUN apt-get update
RUN apt-get install python3 -y
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install pysqlite3
WORKDIR /spgr2
COPY . /spgr2
RUN pip3 install --requirement /spgr2/requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["./app.py"]