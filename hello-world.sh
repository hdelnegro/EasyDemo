#!/bin/bash
zenity --info --text="System information:\n Current User: $USER\n Hostname: $HOSTNAME\n IP Addresses: $(ip addr show ens3 | grep 'inet' | cut -d ' ' -f 6)"