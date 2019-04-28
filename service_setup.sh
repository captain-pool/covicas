#! /bin/bash

pram=$(tr -d '\r' <<< "$1")
echo $pram
if [ "$1" == "install" ];
then
#sudo cp service/covicas.service /etc/systemd/system/covicas.service
#sudo systemctl start covicas
echo "install"
elif [ "$1" == "uninstall" ];
then
#sudo systemctl stop covicas
#sudo rm /etc/systemd/system/covicas.service
echo "uninstall"
fi
