#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
import sys
import os

sys.argv
if len(sys.argv) == 3:
     key = sys.argv[1]
     ip = sys.argv[2]
else:
     print "sys.argv length wrong,please check it"
     sys.exit(0)
class zabbix_tools:

        def __init__(self):
                self.url="http://114.119.10.166/api_jsonrpc.php"
                self.header={"Content-Type": "application/json"}
                self.authID=self.user_login()

        def user_login(self):
                data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": "",
                        "password": ""
                        },
                    "id": 0
                    })
                request = urllib2.Request(self.url,data)
                for key in self.header:
                    request.add_header(key,self.header[key])
                try:
                    result = urllib2.urlopen(request)
                except URLError as e:
                    print "Auth Failed, Please Check Your Name And Password:",e.code
                else:
                    response = json.loads(result.read())
                    authID = response['result']
                    result.close()
                    return authID

        def get_data(self,data,hostip=""):

                request = urllib2.Request(self.url,data)
                for key in self.header:
                    request.add_header(key,self.header[key])
                try:
                    result = urllib2.urlopen(request)
                except URLError as e:
                    if hasattr(e, 'reason'):
                        print 'We failed to reach a server.'
                        print 'Reason: ', e.reason
                    elif hasattr(e, 'code'):
                        print 'The server could not fulfill the request.'
                        print 'Error code: ', e.code
                    return 0
                else:
                    response = json.loads(result.read())
                    result.close()
                    return response


        def delete_items(self,itemids):

                print 'delete'
		data = json.dumps(
                {
                        "jsonrpc":"2.0",
                        "method":"item.delete",
                        "params": itemids,
                        "auth":self.authID,
                        "id":2
                })

                res = self.get_data(data)
		print res
                return res

        def get_hostids(self,ip):

                data = json.dumps(
                {
                        "jsonrpc":"2.0",
                        "method":"host.get",
                        "params":{
                                "output":"extend",
                                "filter":{
                                    "host": ip
                                }
                            },
                        "auth":self.authID,
                        "id":2
                })
                res = self.get_data(data)['result']
                hostids = []
                for i in range(len(res)):
                        hostids.append(res[i]['hostid'])
                return  hostids

        def get_itemids(self,key,ip):

                hostids = self.get_hostids(ip)
                data = json.dumps(
                {
                        "jsonrpc":"2.0",
                        "method":"item.get",
                        "params":{
                                "output":"shorten",
                                "search": {"key_": key},
                                "hostids": hostids,
                                "limit": 10
                        },
                        "auth": self.authID,
                        "id":2
                })
                
                itemids = []
                res = self.get_data(data)['result']
                for i in range(len(res)):
                        itemids.append(res[i]['itemid'])
                return  itemids

	def get_history(self,key,ip):

                itemids = self.get_itemids(key,ip)
                print itemids
               # print key
                data = json.dumps(
                {
                        "jsonrpc":"2.0",
                        "method":"history.get",
                        "params":{
                                "output":"extend",
                                "itemids": itemids,
                              #  "search": {"clock": date},
                                 "sortfield": "clock",
                                 "sortorder": "DESC",
                                "limit": 1
                        },
                        "auth":self.authID,
                        "id":2
                })
                res = self.get_data(data)['result']
                historys = []
                for i in range(len(res)):
#                        print i
                        historys.append(res[i]['value'])
                return  historys
	def get_trigger(ip):

		{
			"jsonrpc": "2.0",
			"method": "trigger.get",
			"params": {
			    	"filter": {
				"host": ["ZABBIX-Server"],
				"description": ["APC: System UPS Global State", "APC: System UPS Load"]
    					},
				"output": "extend"
				},
		"auth": "6f38cddc44cfbb6c1bd186f9a220b5a0",
		"id": 2
		}

def main():
        test = zabbix_tools()
#        print test.user_login()
#	print 'start'
        print test.get_hostids("125.88.158.50")
#        print test.get_data("vfs.fs.size[/,total]","125.88.158.50")
#   itemids = test.get_itemids("vfs.fs.size[/,total]",["120.147.208.71","119.147.216.8","119.147.137.212",])
#        print test.get_itemids("net.if.out[eth0]","119.147.137.212")
#       	print  'two'
#print itemids
#        print test.delete_items(itemids)
        print test.get_history(key,ip)
#	print 'end'

if __name__ =="__main__":
        main()
