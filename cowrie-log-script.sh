#!/bin/bash
while true; do
    filename=$(ls /var/log/containers/ | grep pf-pot)
    if [[ -z "$filename" ]]; then
        sleep 5
        continue
    fi
    
    cp /var/log/containers/"$filename" /persistent-volumes/honeypot-logs/cowrie.log
    sleep 5
done