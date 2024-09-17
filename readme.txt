/usr/local/bin/piradio

/etc/lircd/*



orange install step
1  sudo apt install mpc mpd
2  edit audio_output at /etc/mpd.conf:
3  auto start by edit /etc/rc.local
        sh '/root/oradio.sh'
4   create at home folder 'oradio.sh'
4  sudo apt install apache2 php
5  put server file at /var/www/html/radio/
    using dolphin fish://root:pass@192.168.x.x/var/www/html/radio/


    amixer -c 3  cset numid=6 37,37
