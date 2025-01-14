#!/bin/sh

while [ "$(hostname -I)" = "" ]; do
  echo -e "\e[1A\e[KNo network: $(date)"
  sleep 1
done
su -s /bin/sh -c "alsamixer -D equal" mpd
echo "I have network"
#mpc play
#/usr/bin/python3   /home/root/iradio.py
#  GNU nano 5.4                                       /root/oradio.sh     
sleep 3
#/usr/bin/python3 /root/iradio.py
#sleep 1
#pkill -9 python
#sleep 1
#/usr/bin/python3 /root/iradio.py
exit 0
