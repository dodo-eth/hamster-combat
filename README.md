1) cd /root
2) [clone repo ](https://github.com/dodo-eth/hamster-combat.git)
3) cd /root/hamstercombat/
2) pip3 install -r requirements.txt
4) mv hamster_sync.service /etc/systemd/system/
5) sudo systemctl daemon-reload
6) systemctl start hasmter_sync.service && systemctl enable hasmter_sync.service
