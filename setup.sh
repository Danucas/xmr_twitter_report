#!/usr/bin/env bash
sudo apt-get -y install python3-requests
sudo apt-get -y install git
git clone https://github.com/danrocus1994/xmr_twitter_report
echo '* 8,12,16 * * * '$HOME'/xmr_twitter_report/xmr_caller.py' | crontab -