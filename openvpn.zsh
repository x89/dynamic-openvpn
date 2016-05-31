#!/usr/bin/env sh

if [[ ! $2 ]]; then
	echo "Usage: ./openvpn.sh ip port"
	exit
fi

ret=`host $1`
if [[ $? != 0 ]]; then
	echo "Invalid host $1"
	exit
fi

sudo openvpn --remote $1 $2 --config /home/napalm/dynamic-vpn/aws2.conf
