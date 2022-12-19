#!/bin/bash

if [[ $USER != "root" ]]; then
    echo "You must be root to run this script."
    exit 1
fi

if [ -f /etc/redhat-release ]; then
    OS="CentOS"
elif [ -f /etc/debian_version ]; then
    OS="Debian"
elif [ -f /etc/lsb-release ]; then
    OS="Ubuntu"
elif [ -f /etc/system-release ]; then
    OS="Amazon Linux"
else
    echo "This script is not supported on this OS"
    exit 1
fi

echo "detected OS is $OS"
echo " "

## If debian based distro is detected
if [ "$OS" == "Debian" ] || [ "$OS" == "Ubuntu" ]; then
    apt-get update -y
    apt install python3 python3-pip git vim python3-venv -y
    mkdir /var/ossec/wodles/custom
    chown -R root:wazuh /var/ossec/wodles/custom*

## If rhel based distro is detected
elif [ "$OS" == "CentOS" ] || [ "$OS" == "Amazon Linux" ]; then
    yum install python3 python3-pip git vim -y
    mkdir /var/ossec/wodles/custom
    chown -R root:wazuh /var/ossec/wodles/custom*
fi

## copy the files to the correct locations
cp -r bin/vuln.py /var/ossec/wodles/custom
cp requirements.txt /var/ossec/wodles/custom

## Configure Python3 env
python3 -m venv /var/ossec/wodles/custom/venv
source /var/ossec/wodles/custom/venv/bin/activate
/var/ossec/wodles/custom/venv/bin/pip3 install --upgrade pip
/var/ossec/wodles/custom/venv/bin/pip3 install -r /var/ossec/wodles/custom/requirements.txt

sha256sum /var/ossec/wodles/custom/vuln.py
