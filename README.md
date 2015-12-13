# service_chaining
IP Project. Service chaining using openflow

This projects aims at implementation of service chaining using Openflow.

Client (Host A) Socket program sends application pdu which contains information of services required by client.

Controller program performs following operations:

1. It decodes signalling informaiton sent by client . As a result of it, controller finds out the services which are requested by client.
2. Finds the location of services from controller database.
3. Finds the shortest path to access those services.
4. Install flows on relevant switches which route packets to services installed at various machines in the network topology.

Once flows are installed a png format image is sent by client towards a destination (Host B).
For demo , I have implemented a transcoder which performs image conversion from png to jpeg format. The purpose of implementing transcoder is to show proper routing of packets between switches towards service location so that image data is properly processed at transcoder and then sent towards destination. The transcoder service is installed at various location in the network. It helped in testing shortest path finding algorithm.

Thus data sent by client (i.e. image) is routed towards service requested by a user (transcoder in this case) where it is received and processed . After processing, data sent towards either destination (Host B) or other services(if requested ) by user.. 

At destination, a server socket programs receives data coming from network.

In case of transcoder, a jped image is retrieved from data.


