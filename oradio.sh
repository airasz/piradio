#!/bin/sh

while [ "$(hostname -I)" = "" ]; do
  echo -e "\e[1A\e[KNo network: $(date)"
  sleep 1
done

echo "I have network"
mpc play
python3   /home/root/iradio.py
#  GNU nano 5.4                                       /root/oradio.sh     
exit 0
