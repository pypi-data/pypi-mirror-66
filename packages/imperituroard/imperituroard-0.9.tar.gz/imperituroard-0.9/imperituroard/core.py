#!/usr/bin/python

import sys
import os
sys.path.append(os.path.abspath("../"))

from imperituroard.projects.messagehub import get_stat
from imperituroard.projects.dns import functions, influxdb
from imperituroard.projects.freewifi import mikrotik

from imperituroard.universal.influxdbdata import Influxdb
import random
import threading



class Ard:
    def __init__(self):
        self.test = "test"
        self.answ = {}


    def send_telegram_message(self, message, chatid, token):
        functions.send_telegr(message, chatid, token)

    def get_modules_status(self):
        stat = functions.get_modules_status()
        return stat

    def get_hostname(self):
        hn = functions.get_hostname()
        return str(hn)

    def ping_check(self):
        resp = functions.check_ping()
        return resp

    def gen_password(self, passlen=8, security=2):
        let = ""
        if (security == 0):
            let = "0123456789"
        elif (security == 1):
            let = "abcdefghijklmnopqrstuvwxyz0123456789"
        elif (security == 2):
            let = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        elif (security == 3):
            let = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
        else:
            let = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        resp = "".join(random.sample(let, passlen))
        return resp

    def gedata_mikr(self, a, user, plist, prt):
        for p in plist:
            try:
                resp1 = mikrotik.get_serial(a, user, p, prt)
                ide = mikrotik.get_identity(a, user, p, prt)
                resp = {"identity": ide, "data": resp1}
                aaa = {a: resp}
                self.answ.update(aaa)
                print (aaa)
            except:
                continue

    def get_serial_mikrotik(self, mlist, plist, user, port):
        num = len(mlist)
        threads = []

        for val in range(0, num):
            try:
               thread1 = threading.Thread(target=self.gedata_mikr, args=(mlist[val], user, plist, port))
               # thread1.setDaemon(True)
               thread1.start()
               threads.append(thread1)
            except:
               self.answ.update({val: "offline"})

        for thread in threads:
            thread.join()
        return self.answ



class ArdUnbound:
    def __init__(self, telegram_token, telegram_chat_id):
        self.test = "test"
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def processes_check(self):
        stat = functions.get_modules_status()
        hostn = functions.get_hostname()
        if stat["unbound"] < 50:
            mess1 = "DNS " + hostn + " ERROR. Some Unbound processes are failed"
            functions.send_telegr(mess1, self.telegram_chat_id, self.telegram_token)

        if stat["bfd_c"] < 6:
            mess2 = "DNS " + hostn + " ERROR. Some BFD processes are failed"
            functions.send_telegr(mess2, self.telegram_chat_id, self.telegram_token)

        if stat["bird"] < 1:
            mess3 = "DNS " + hostn + " ERROR. BGP IPv4 process failed"
            functions.send_telegr(mess3, self.telegram_chat_id, self.telegram_token)

        if stat["zabbix"] < 1:
            mess4 = "DNS " + hostn + " ERROR. Zabbix Agent IPv4 process failed"
            functions.send_telegr(mess4, self.telegram_chat_id, self.telegram_token)

        if stat["bird6"] < 1:
            mess5 = "DNS " + hostn + " ERROR. BGP IPv6 process failed"
            functions.send_telegr(mess5, self.telegram_chat_id, self.telegram_token)


class ArdInflux:
    def __init__(self, influxurl):
        self.influxurl = influxurl

    def unbound_stat_to_influx(self):
        hostname = functions.get_hostname()
        data = functions.get_data_from_unbound_stat()
        influxdb.push_unbound_metrics(data, self.influxurl, hostname)

class Mhub:
    def __init__(self, stat_url, influx_url):
        self.stat_url = stat_url
        self.influx_url = influx_url

    def push_stat_to_influx(self):
        data = get_stat.prepare_data_from_staturl(self.stat_url)
        influx_connector = Influxdb(self.influx_url)
        influx_connector.data_to_influx(data)
