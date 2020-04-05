#!/usr/bin/python3
"""Tweety Api handler module"""


from hashlib import sha1
import hmac, random, codecs, time, requests
from urllib.parse import quote
import base64
import os
import json


class Tapi:
    """
    Tapi class, contain methods that build Twitter Api requests
    methods:
    check the methods with dir(Tapi)
    """
    def __init__(self, cons_k, cons_s, tok_k, tok_s):
        """
        Initialize Tapi object with credential keys
        """
        self.__cons_k = cons_k
        self.__cons_s = cons_s
        self.__tok_k = tok_k
        self.__tok_s = tok_s

    @property
    def cons_k(self):
        """Consumer Api key"""
        return self.__cons_k

    @property
    def cons_s(self):
        """Consumer secret key"""
        return self.__cons_s

    @property
    def tok_k(self):
        """Token Api key"""
        return self.__tok_k

    @property
    def tok_s(self):
        """Token secret key"""
        return self.__tok_s

    def gen_sig(self, dic, url="", method=""):
        """This method generates the authorization signature"""
        keys = [st for st in dic.keys()]
        keys = sorted(keys)
        out_s = ""
        for attr in keys:
            key = quote(bytes(attr, "ascii"), safe="")
            out_s += key + "="
            out_s += quote(bytes(dic[attr], "UTF-8"), safe="")
            out_s += "&"
        out_s = quote(bytes([ord(x) for x in out_s[:-1]]), safe="")
        url = quote(bytes([ord(x) for x in url]), safe="")
        par_str = "&".join([method, url, out_s])
        par_str = bytes([ord(x) for x in par_str])
        sig_key = quote(bytes([ord(x) for x in self.__cons_s]), safe="") + "&"
        sig_key += quote(bytes([ord(x) for x in self.__tok_s]), safe="")
        sig_key = bytes([ord(x) for x in sig_key])
        hashed = hmac.new(sig_key, par_str, sha1)
        hashed = codecs.encode(hashed.digest(), "base64").rstrip(bytes([10]))
        hashed = quote(hashed, safe="")
        return hashed

    @property
    def nonce(self):
        """Nonce:
         returns the actual request nonce generated string"""
        return self.__nonce

    def gen_nonce(self):
        """This method generates the nonce string"""
        nonce = lambda length: list(filter(lambda s: chr(s).isalpha(), base64.b64encode(os.urandom(length * 2))))[:length]
        nonce = codecs.encode(bytes(nonce(32)), "base64").rstrip(bytes([10]))
        nonce = ''.join([chr(x) for x in nonce])[:-1]
        self.__nonce = nonce
        return self.__nonce

    def get_time(self):
        """To get the request time parameter"""
        self.__time = str(int(time.time()))
        return self.__time

    def gen_header(self, sig_data):
        """Contructs a header for the request"""
        keys = [st for st in sig_data.keys()]
        keys = sorted(keys)
        header_str = "OAuth "
        for par in keys:
            header_str += par
            header_str += '="'
            header_str += sig_data[par]
            header_str += '", '
        header_str = header_str[:-2]
        return header_str


    def get_user(self, par):
        """Get an User info by passing a user id"""
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.cons_k,
                    "oauth_token": self.tok_k,
                    "oauth_version": "1.0"
        }
        pars = par
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/users/lookup.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head, 'content-type': 'application/json'}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak

    def follow_user(self, id=""):
        """Follows an user by passing an id"""
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.cons_k,
                    "oauth_token": self.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"user_id": id, "follow": "true"}

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/friendships/create.json'
        sign = self.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head, 'content-type': 'application/json'}
        ak = requests.post(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak

    def get_followers(self, id="", cursor=None):
        """Get a follower info"""
        self.gen_nonce()
        sig_data = {#"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0"
                    }

        pars = {"user_id": id, "count": "100", "skip_status": "false"}
        if cursor != None:
            pars["cursor"] = cursor

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/followers/list.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak


    def search_tweets(self, query=""):
        """Searches tweets by query"""
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0"
                    }

        pars = {"q": query}

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/search/tweets.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak


    def search_users(self, query=""):
        """search multiple users by query"""
        self.gen_nonce()
        sig_data = {"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0",
                    "q": query,
                    "page": "5"
                    }
        ur = 'https://api.twitter.com/1.1/users/search.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign
        del sig_data["q"]
        del sig_data["page"]
        del sig_data["include_entities"]
        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        #print("\n", heads, "\n")
        ur += "?include_entities=true"
        #print("\nurl: ", ur)
        ak = requests.get(ur, headers=heads, params={'q': query, 'page': '5'})
        print(ak.status_code)
        return ak

    def update(self, message):
        """Send an 'update' containing 'message' parameter"""
        self.gen_nonce()
        sig_data = {"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0",
                    "status": message
                    }
        ur = 'https://api.twitter.com/1.1/statuses/update.json'
        sign = self.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign
        del sig_data["status"]
        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        #print("\n", heads, "\n")
        ur += "?include_entities=true"
        print("\nurl: ", ur)
        ak = requests.post(ur, headers=heads, params={'status': message})
        print(ak.status_code)
        return ak




def get_user_followers(id, cursor):
    res = api.get_followers(id, cursor)
    return res

def get_api():
    return api

def follow(id=""):
    res = api.follow_user(id)
    return res

def get_tweets(query):
    res = api.search_tweets(query)
    return res.json()


def get_users(query):
    res = api.search_users(query).json()
    for i in range(len(res) - 1):
        p = "\033[32m"
        d = "\033[0m"
        print("{}:{:15}, {}".format(
            p+str(i)+d, res[i]["name"], res[i]["screen_name"]))
    return res

def steal_followers(name=""):
    users = api.get_user({"screen_name": name}).json()
    for i in users:
        print(i["name"], i["screen_name"])
    pos = int(input("Choose an index: "))
    user = users[pos]
    print("Stealing from: ", user["screen_name"])
    cursor = None
    while True:
        res = get_user_followers(str(user["id"]), cursor)
        if res.status_code != 200:
            print(res.text)
            break
        folls = res.json()
        uss = folls["users"]
        res = follow_users(uss)
        cont = input("Continue ?")
        cursor = str(folls["next_cursor"])

def follow_users(users):
    unfoll = []
    for us in users:
        following = us["following"]
        col = "\033[31m" if following == False else "\033[32m"
        if following is False:
            print(us["name"].encode('utf-8'), col, following, "\033[0m")
            unfoll.append(str(us["id"]))
    for i, us in enumerate(unfoll):
        res = follow(str(us))
        usr = res.json()
        if res.status_code != 200:
            print(res.content)
        else:
            print("Now Following: ", usr["screen_name"], "\nremaining: ", len(unfoll) - i)
        for i in range(5):
            time.sleep(1)
            print("Time elapsing: ", 5 - i, "\r", end="")
        print()