#!/usr/bin/env python
#coding: utf-8

import json
import prettytable
import requests
import argparse
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
            request = self.session.get(self.url)
            if request.status_code != 200:
                print(u'[-] 不能访问ceye.io')
                exit(1)
            response = request.text
            if 'meta' not in response:
                print(u'[-] 没有数据')
            data = json.loads(response)
            if data['meta']['code'] == 200 and data['meta']['message'] == 'OK' and data['data']:
                return data['data']
        except KeyboardInterrupt:
            exit(1)
        except:
            pass
                

    def run(self):
        table = prettytable.PrettyTable()
        table.field_names = ['序号', 'URL', '远程地址', '访问时间']
        index = 1
        created_at = []
        while True:
            try:
                data = self.get_log()
                for row in data:
                    if row['name'] and row['remote_addr'] and row['created_at'] and (row['created_at'] not in created_at):
                        created_at.append(row['created_at'])
                        table.add_row([index, row['name'], row['remote_addr'], row['created_at']])
                        index += 1
                print(table)
                sleep(10)
            except KeyboardInterrupt:
                exit(1)
            except:
                pass

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--token', required=False, help="Ceye.io API token, geting on Ceye.io user's profile")
    parser.add_argument('-t', '--type', help='Ceye log type, dns or http, default http')
    parser.add_argument('-f', '--filter', type=str, help = 'filter args')
    args = parser.parse_args()

    cmd_args = {k:v for k, v in vars(args).items() if v}

    default = {
        'token': '4b61de125d55f87917b24f898d5d817f',
        'type': 'http',
        'filter': ''
    }
    return ChainMap(cmd_args, default)

def main():
    args = get_arguments()
    CeyeDNSLog(args).run()

if __name__ == '__main__':
    main()