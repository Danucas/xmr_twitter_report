#!/usr/bin/env bash
# Setup the environment to run the python script
# Scheduling with crontab at 8, 12, and 14
sudo apt-get -y install python3-requests
sudo apt-get -y install git
git clone https://github.com/danrocus1994/xmr_twitter_report
echo '* 8,12,16 * * * '$HOME'/xmr_twitter_report/xmr_caller.py' | crontab -