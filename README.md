# P1-biteDistributedSystem
Project 1 - CECS 327

To compile the code, make sure to be in the correct directory(ex: multicast and unicast)

Docker desktop must be installed.

**Do not include the $ and the '-> ...' **

First, create network.

$ docker network create --driver bridge Proj1-distributed-network

For multicast, execute the following commands in this order in the terminal:

$ docker volume create network_logs -> to store network logging data

$ docker build -t multicast-master -f Dockerfile.MCmaster . -> build master image

$ docker build -t multicast-node -f Dockerfile.MCnode . -> build node image

$ docker run --rm -d --name multicast-receiver1 --network Proj1-distributed-network -v network_logs:/app/logs multicast-master

$ docker run --rm -d --name multicast-receiver2 --network Proj1-distributed-network -v network_logs:/app/logs multicast-master

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 1 "Hello Multicast World! From node 1"

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 2 "Hello Multicast World! From node 2"


output for node connections are shown in the terminal. Output for network logging shown in the volume in docker desktop. Output for receivers are located in docker logs.






