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

# copy and activate our systemd and desktop definitions
echo "Copy and activate our systemd and desktop definitions..."
echo "=========================="
# hateCircuit service
mkdir -p /home/pi/.config/autostart
cp ./hateCircuit.desktop /home/pi/.config/autostart/hateCircuit.desktop
# pythonShutdown service
cp ./pythonShutdown.service /lib/systemd/system/pythonShutdown.service
chmod 644 /lib/systemd/system/pythonShutdown.service

# reload and enable systemd services
systemctl daemon-reload
systemctl enable pythonShutdown.service

# replace splash screen with our own
echo "Replacing splash screen with our own..."
echo "=========================="
mv /usr/share/plymouth/themes/pix/splash.png /usr/share/plymouth/themes/pix/splash.png.bak
cp ./splash.png /usr/share/plymouth/themes/pix/splash.png
plymouth-set-default-theme --rebuild-initrd pix

# stop task bar from loading - MUST be using X11
echo "Stopping the taskbar from loading"
echo "=========================="
sed -i 's/@lxpanel-pi/#@lxpanel-pi/' /etc/xdg/lxsession/rpd-x/autostart

# done
echo "Done. Rebooting now"
echo "=========================="
reboot
