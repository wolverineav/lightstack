from collector.models import *
from collector.configdata import *
#REST calls to FloodLight
import json
import urllib2

def getSwitchList(hostIP):
    url = 'http://{FLHostIP}:8080/wm/core/controller/switches/json'.format(FLHostIP=hostIP)
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        responseText = response.read()
        return responseText
    except urllib2.HTTPError, e:
        raise e

def refreshSwitchList():
    swList = getSwitchList(FloodLight.hostIP)
    swList = json.loads(swList)
    for sw in swList:
        #create switches in database
        swtype = 'pSwitch'
        if 'vSwitch' in sw['description']['hardware']:
            swtype = 'vSwitch'
        new_sw, created = Switch.objects.get_or_create(
                dpid = sw['dpid'],
                defaults = {
                    'switchType' : swtype,
                    'dpid' : sw['dpid'],
                    'inetAddr' : sw['inetAddress'],
                })
        if created:
            print sw['dpid'] + ' created'
        #create ports per switch
        for port in sw['ports']:
            new_port, created = Port.objects.get_or_create(
                    hwAddr = port['hardwareAddress'],
                    defaults = {
                        'switch' : new_sw,
                        'hwAddr' : port['hardwareAddress'],
                        'portNumber': port['portNumber'],
                    })
            if created:
                print 'port ' + new_port.hwAddr + ' created'

