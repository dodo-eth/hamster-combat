1) clone repo 
2) pip3 install -r requirements.txt
3) mv folder to /root/hamstercombat/
4) mv hamster_sync.service /etc/systemd/system/
5) sudo systemctl daemon-reload
6) systemctl start hasmter_sync.service && systemctl enable hasmter_sync.service