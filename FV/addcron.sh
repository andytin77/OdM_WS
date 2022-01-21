crontab -r
crontab -l | { cat; echo "*/3 * * * * cd /home/pi/ && ./vedirect.sh > /dev/null 2>&1" ; } | crontab -
sudo service cron restart
