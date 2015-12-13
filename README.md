# service_chaining
IP Project. Service chaining using openflow

This projects aims at implementation of service chaining using Openflow.

Client Socket program sends application pdu which contains information of services required by client.

Controller program performs following operations:

1. It decodes signalling informaiton sent by client . As a result of it, controller finds out the services which are requested by client.
2. Finds the location of services from controller database.
3. Finds the shortest path to access those services.
4. Install flows on relevant switches which route packets to services installed at various machines in the network topology.

Once flows are installed a png format image is sent by client.
For demo , I have implemented a transcoder which performs image conversion from png to jpeg format. A The purpose of implementing transcoder is to show proper routing of packets between switches towards service location so that image data is properly processed at transcoder and then sent towards destination.

At destination, a server socket programs receives data coming from network and retrieves the image with changed format.


