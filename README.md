![Screenshot](/pihidproxy.jpg?raw=true "pihidproxy")

Bridge a Bluetooth keyboard to USB using a Raspberry Pi Zero W.

The keycodes are based on a Logitech K380, but can be easily edited to suit other devices.

The usage IDs can be found on page 53 of this document:
https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

Forked from https://github.com/mikerr/pihidproxy

Install requirements:

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install python-pip
    sudo pip install evdev

Enable dwc2 driver (USB host):

    echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
    echo "dwc2" | sudo tee -a /etc/modules
    echo "libcomposite" | sudo tee -a /etc/modules

Locate device's MAC address:

    sudo hcitool scan

Pair, Connect and Trust:

    sudo bluetoothctl

    agent on
    scan on
    pair [MAC Address]
    connect [MAC Address]
    trust [MAC Address]

Example usage:

    sudo setuphid.sh
    tmux new-session -d -s "hid-proxy" 'sudo python proxy.py'
