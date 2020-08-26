#!/usr/bin/env python
#coding: utf-8

import json
import requests
import argparse
import hashlib
from time import sleep
from typing import ChainMap


class CeyeDNSLog(object):
    def __init__(self, args):
        self.url = 'http://api.ceye.io/v1/records?token={}&type={}&filter={}'
        self.type = args['type']
        self.token = args['token']
        self.filter = args['filter']
        self.url = self.url.format(self.token, self.type, self.filter)
        self.session = requests.Session()

    def get_log(self):
        try:
            request = self.session.get(self.url, timeout = 5)
            if request.status_code != 200:
                print(u'[-] 连接出错：{}'.format(request.status_code))
                #exit(1)
            response = request.text
            if 'meta' not in response:
                print(u'[-] 没有获取到数据')
            data = json.loads(response)
            if data['data']:
                return data['data']
        except TimeoutError:
            print(u'连接CEYE超时')
                

    def run(self):
        index = 1
        row_dict = {}
        while True:
            try:
                data = self.get_log()
                if data:
                    for row in data:
                        data_hash = hashlib.md5((row['name'] + row['remote_addr'] + row['created_at']).encode()).hexdigest()
                        if data_hash not in row_dict:
                            row_dict[str(data_hash)] = '\t'.join([str(index), row['name'], row['remote_addr'], row['created_at']])
                            index += 1
                            print(row_dict[data_hash])
                sleep(10)
            except KeyboardInterrupt:
                exit(1)
            except Exception as e:
                print(e)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--token', required=False, help="Ceye.io API token, geting on Ceye.io user's profile")
    parser.add_argument('-t', '--type', help='Ceye log type, dns or http, default http')
    parser.add_argument('-f', '--filter', type=str, help = 'filter args')
    args = parser.parse_args()

    cmd_args = {k:v for k, v in vars(args).items() if v}

    default = {
        'token': 'your token',
        'type': 'http',
        'filter': ''
    }
    return ChainMap(cmd_args, default)

def main():
    args = get_arguments()
    CeyeDNSLog(args).run()

if __name__ == '__main__':
    main()
