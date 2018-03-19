# caffè! to influx connector

[**caffè!**](http://projectcaffe.bplaced.net/) is a firmware running on microcontrollers, offering support for dual PID-control, pressure profiling and scripted programs for espresso machines (see [features](http://projectcaffe.bplaced.net/features_caffe.html)).
This turns your espresso machine into a beast :)

Running on an [ito](https://www.kaffee-netz.de/threads/ito.102112/) it connects to wifi networks via the built in  ESP8266 module and broadcasts its readings via telnet (after requesting it with telnet command _MCr\r\n_).

This connector queries the telnet interface and loads it into a [influxDB](https://www.influxdata.com), making it easy to visualize with [grafana](https://grafana.com). Perfect for data nerds to collect some statistics of their coffee cravings.

While the espresso machine is turned off the script queries the ito module every minute, once it turns on it writes the readings into influx every 10 seconds and while the coffee extraction is running it writes every reading into the database (2 readings per second).

## Getting Started

**Requirements**
Correct installation of the ito module is necessary.
python
Installed influxDB.
Grafana optional, or other visualization platform

**Running the script**
Replace the variables for the server connection and the IP of the ito module and run it (e.g. with cron at reboot).

I am running completely in Docker (swarm), running the python script itself in [OpenFaas](https://www.openfaas.com/) on a raspberryPi 3. I may release a Docker stack as well at some point.

![Screenshot](screenshot.jpg?raw=true "Screenshot")