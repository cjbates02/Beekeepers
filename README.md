# Beekeepers
## Overview:
A microservices oriented approach to hosting and monitoring a variety of honeypots. These honeypots are hosted on a kubernetes cluster in pods using docker engine for the container runtime interface. The logs for each honeypots are continously monitored such that the logs are sent to an ELK stack that is also deployed on the same cluster. Additionally, there is a packet sniffer listening on the interface of the node hosting the honeypots where packet analysis is performed. There is also a custom web ui that is designed to provide a birds eye view of the entire applications, allowing users to drill into each honeypot and see recent activity, state, and a record of logs without having to using the kube api directly. Currently we are using two honeypots, one is an open source ssh honeypot called cowrie, and the other is a fake pf sense log in screen. 

## How we are hosting this securely
The system is deployed on site in a kubernetes cluster with two nodes. The first node is a bare metal server hosted in a DMZ that hosts the honeypot pods, and the second node is a bare metal server located in our LAN that hosts our monitoring pods. There is a pf sense firewall seperating the two nodes with rules configured to limit communication between the two nodes to as little as possible. Additionally, there are network policies enforced within the cluster using calico as our network plugin that restricts communication between the DMZ node and the LAN node. Metallb is configured as the load balancer for the cluster that assigns a unique ip address to each of our honeypot pods, enabling us to expose the exact ports we want and forward traffic more securely. This was as apposed to using node port services where we were limited to using a high range of ports on the same ip address as the node running the honeypot pods.

## Tech Stack

### Platform
1. Kubeadm to congfigure the bare metal cluster.
2. Calico as the network plugin for the cluster.
3. Docker engine as the container runtime interface.
4. Metallb as a bare metal load balancer.
5. Elasticsearch, logstash, and kibana for monitoring and analysis

### Web UI
1. Flask for the web framework
2. HTML / CSS / JavaScript

### Packet Analysis

1. Scapy python library
2. TCP Dump as the packet sniffer




