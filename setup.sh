#!/bin/bash

# Setup script to install our required software and 
# configure services etc.

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./setup.sh"
  exit 1
fi

# update and upgrade existing packages
echo "Upgrading existing packages"
echo "=========================="
apt update && apt dist-upgrade -y && apt autoremove -y

# install pip packages
echo "Installing required pip packages"
echo "=========================="
pip3 install socialapis-sdk --break-system-packages
pip3 install textblob --break-system-packages
pip3 install Unidecode --break-system-packages
pip3 install RPi.GPIO --break-system-packages

# copy and activate our systemd definitions
echo "Copy and activate our systemd definitions..."
echo "=========================="
# hateCircuit service
mkdir -p /home/pi/.config/autostart
cp ./hateCircuit.desktop /home/pi/.config/autostart/hateCircuit.desktop
# pythonShutdown service
cp ./pythonShutdown.service /lib/systemd/system/pythonShutdown.service
chmod 644 /lib/systemd/system/pythonShutdown.service

# reload and enable
systemctl daemon-reload
systemctl enable hateCircuit.service
systemctl enable pythonShutdown.service

# done
echo "Done. Rebooting now"
echo "=========================="
reboot
