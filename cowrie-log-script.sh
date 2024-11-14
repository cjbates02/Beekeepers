#!/bin/bash
while true; do
    filename=$(ls /var/log/containers/ | grep cowrie)
    formatted_date=$(date +"%Y-%m-%d %H:%M:%S") 
    if [[ -z "$filename" ]]; then
        sleep 5
        continue
    fi
    
    sudo cp /var/log/containers/"$filename" /persistent-volumes/honeypot-logs/cowrie.log
    sudo chmod o+r /persistent-volumes/honeypot-logs/cowrie.log
    sleep 5
done
