#start with a python base-image
FROM python:3.7-alpine

WORKDIR /app

#install required python packages
RUN pip install paho-mqtt
RUN pip install influxdb

#copy the python script into the container
COPY . .

#set environment variable (for testing)
ENV INFLUXDB_DATABASE "databus_values"

#set start command for container
CMD [ "python", "-u", "main.py" ]
