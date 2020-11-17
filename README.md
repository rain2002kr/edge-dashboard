# Grafana-Dashboard-Demo
This application was originially created by Benjamin Richter and was edited for showcasing a multideployment- and multicontainer-application with Node-Port, Cluster-IP, Enviroment Variables, Persistent Storage and Databus-Service.

This is an example application to showcase how to connect to the SIMATIC Edge Databus (MQTT Broker), subscribing to topics using the databus-service, writing the recieved values to a InfluxDB and visualizing it with a Grafana Dashboard. 

This application consists of three services. 

## Data-Collector
The Data-Collector connects to the SIMATIC Edge Databus (MQTT Broker) using the Eclipse PAHO MQTT Client library for Python. The MQTT Client subribes to topics on the Databus and writes them to a InfluxDB.

## InfluxDB

The InfluxDB stores the values collected by the Data-Collector as Time-Series-Data.

## Grafana

The Grafana-Dashboard uses the InfluxDB as a Data-source and visualizes the data in a chart.


## Workflow Building and Deploying Application

__1. Step__: Build docker images:
```
docker-compose build
```

---

__2. Step__: Upload App with Edge Publisher in Industrial Edge Management (IEM)

---

__3. Step__: Configure Soutbound-Connectivity and Databus

---

__4. Step__: Edit env-config.json

---

__5. Step__: Install Edge App with env-config.json file

---

__6. Step__: Configure Grafana
- Open Grafana
- Login: Username: admin, Password: admin
- Add data source: InfluxDB
- Enter InfluxDB URL: http://influxdb:8086
- Enter Database: Varaiable "INFLUXDB_DATABASE" in env-config.json 
- Create Dashboard

