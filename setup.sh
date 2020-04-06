#!/usr/bin/env bash
# Setup the environment to run the python script
# Scheduling with crontab at 8, 12, and 14
if [ $# -lt 4 ];then
	echo "Usage ./setup <consumer-key> <consumer-secret> <token> <token-secret>"
else
	mkdir $HOME/keys
	echo "CONS_KEY="$1 >> $HOME/keys/sec_twitter_keys
	echo "CONS_SEC="$2 >> $HOME/keys/sec_twitter_keys
	echo "TOKE_KEY="$3 >> $HOME/keys/sec_twitter_keys
	echo "TOKE_SEC="$4 >> $HOME/keys/sec_twitter_keys
	#sudo apt-get -y install python3-requests
	#sudo apt-get -y install git
	#git clone https://github.com/danrocus1994/xmr_twitter_report
	#echo '* 8,12,16 * * * '$HOME'/xmr_twitter_report/xmr_caller.py' | crontab -
fi