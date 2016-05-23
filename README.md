AWS Dynamic VPN
=====

Simple script(s) to dynamically spin up an EC2 instance from an AMI which you
can use to run OpenVPN over as and when you need it, with a different IP
each time, with potentially configrable parameters such as its location.


This is just a simple example for others to build on, feel free to issue pull
requests, there's much that can be improved on.

Regenerating server/client keys each run, better catching of script termination,
hooking into systemd for multi-user/shutdown.target, randomisation of port
number (or port 443), and so on. Orchestration could be done with your favourite
config management tool.
