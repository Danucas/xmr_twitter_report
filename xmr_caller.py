#!/usr/bin/python3
"""
This module call gecko API process the response 
and sends a Twitter alert with the monero state updates
"""


from twitter_api import Tapi
import requests
import json
import os


response = requests.get("https://api.coingecko.com/api/v3/coins/monero")
xmr_data = json.loads(response.text)
usd_exchange = xmr_data["market_data"]["current_price"]["usd"]
btc_exchange = xmr_data["market_data"]["current_price"]["btc"]
market_cap = float(xmr_data["market_data"]["market_cap"]["usd"] / 1000000)
message = 'Current Monero price\n' + '1 XMR:  ' +\
			'USD $ ' + str(usd_exchange) + '\n\t' +\
			'BTC $ ' + str(btc_exchange) + '\n\n' +\
			'Market Capitalization\n$ ' + '{:.2f}'.format(market_cap) + ' M\n' +\
			'$XMR #XMR #Monero #Cryptocurrency'
with open('test_file', "w") as test:
	test.write(message)

with open(os.getenv("HOME") + "/keys/sec_twitter_keys", "r") as keys:
	keys = keys.read()
keys = keys.split('\n')[:-1]

api = Tapi(keys[0].split("=")[1], 
			keys[1].split("=")[1], 
			keys[2].split("=")[1], 
			keys[3].split("=")[1])
api.update(message)
