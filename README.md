# Charging Station Management System - CSMS

## Introduction 

Charging Station Management System(CSMS) is the server which connects with the websocket based connection with charging stations based on OCPP 2.0.1.
The application for monitoring and controlling electric vehicle chargers.

This repository is the template for starting a base for OCPP `2.0.1`.

The source code is divided between different parts, which are

- Charge Point Node
- CLI helpers
- Core
- Manager
- SSE



### Terms

    -  "charge point node" the same as the "charge point service" on the screen
    -  "manager" the same as the "management system" on the screen
    -  "events" are the messages from the "charge point node" to the "manager"
    -  "tasks" are the messages from the "manager" to the "charge point node"

### How does it work

#### Operations initialized by physical charging station

    -  "charge point node" accepts connection from the physical charging station
    -  "charge point node" accepts data from the physical charging station
    -  "charge point node" prepares an "event" and puts it into the queue (see the screen)
    -  "manager" consumes data and handle it as an "event"
    -  "manager" has a monopoly access to the database
    -  after an "event" has handled, the "manager" prepares "task" and puts it into the queue
    -  "charge point node" consumes "task" and executes the one (replies to the physical charging station)


## Context 

This is based on client-server architecture, here CSMS is the server and the Charging Station is the client.

The physical charging station establishes websocket connection and interacts with the management system.

The server consists of two parts: **charge point** service and **management system**.

Charge point service is responsible for the direct interaction with physical charging stations.

Management system is  responsible for the business logic (such as permissions, charging process control, payments, etc). It knows nothing about how the charge point service works.

Both parts interact with each other through the queue and durable AMQP protocol. The advantage of the approach is high scalability.

**Example**: Say, an operation initiated by a physical charging station as an event.
Charge point service accepts data, prepares event, and puts it into the queue. The management system accepts it, takes the decision on how to process a given event (regarding predefined conditions and database state), prepares a reply as a task , and puts data into the queue. All existing charge point services consume tasks, check if the charge point, specified
in the task, is connected to the host and if so, executes the task or just sends data to the physical charging station.

And vice versa with operations initiated by UI. The user sends data into the management system. The system prepares data as a task and puts it into the queue. All charge point services consume the task and further actions happen as described before.

## Pre-requisites

- Docker 24.0.7
- Python 3.11

## Installation

1. Clone the source code

```
git clone https://github.com/lakebrains-ind/ocpp2.0.1.git
```

2. Change directory to the `ocpp2.0.1` folder.

3. Start the docker containers using the `docker-compose.yml` file, with the command

```
docker compose up --build
```

> Note: Make sure you have docker installed

4. CSMS Setup is all done!

## Using

For real, you can do 
- Connect your simulator or hardware with the webosocket connection mentioned in the `.env` file. The default port for connection is `3000`.

The websocket connection URL is `ws://localhost:3000/ocpp` for local connection.  

For simulating, the functioning do the task below

- Test it with the available test modules in the directory `backend/charge_point_node/tests`

- In the `tests` directory, there is a a `charging.py` file, by default, the test only sends a ***boot notification*** request.

> Note: you can find some of the basic message of OCPP 2.0.1 in this test file.

## Cleaning

For development purpose, you can clean the tables Charge Points, Transactions and Locations by executing the script.

```python backend/charge_point_node/tests/clean.py```


#### Operations initialized by UI

    -  "manager" accepts request from the UI
    -  "manager" prepares "task" and puts it into the queue
    -  "charge point node" consumes "task" and executes the one (sends data to the physical charging station)


## Documentation on the OCPP 2.0.1

For more information about the OCPP 2.0.1, refer to the directory `OCPP-2.0.1_-all_files_1-1` in the source code. It contains the information available when this template was created.

For latest information, refer to [OCA Alliance](https://openchargealliance.org/my-oca/ocpp/).
## Tech Stack
- Python3.11, FastAPI 
- Rabbitmq
- Postgresql
- Sqlachemy
- Docker, Docker-Compose

