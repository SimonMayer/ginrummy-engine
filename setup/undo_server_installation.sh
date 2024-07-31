#!/bin/bash

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Stop and disable the ginrummy-front service
systemctl stop ginrummy-front
systemctl disable ginrummy-front

# Remove the ginrummy-front systemd service file
rm /etc/systemd/system/ginrummy-front.service

# Reload systemd to apply changes
systemctl daemon-reload

# Remove Nginx configuration
rm /etc/nginx/sites-enabled/ginrummy-front
rm /etc/nginx/sites-available/ginrummy-front

# Restart Nginx to apply changes
systemctl restart nginx

# Remove the ginrummy-front directory
rm -rf /root/ginrummy-front
