# P1-biteDistributedSystem
Project 1 - CECS 327

To compile the code, make sure to be in the correct directory(ex: multicast and unicast)

Docker desktop must be installed.

For multicast, execute the following commands in this order in the terminal:

$ docker volume create network_logs -> to store network logging data

$ docker build -t multicast-master -f Dockerfile.MCmaster . -> build master image

$ docker build -t multicast-node -f Dockerfile.MCnode . -> build node image

$ docker run --rm -d --network Proj1-distributed-network --name master -v network_logs:/app/logs multicast-master  -> run container for master, output shown in logs

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 1 "Message from node 1" -> runs node 1

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 2 "Message from node 2" -> runs node 2

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 3 "Message from node 3" -> runs node 3

$ docker run --rm --network Proj1-distributed-network -v network_logs:/app/logs multicast-node 4 "Message from node 4" -> runs node 4

output for node connections are shown in the terminal. Output for network logging shown in the volume in docker desktop.






