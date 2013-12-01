from collector.models import *
from collector.configdata import *
#REST calls to FloodLight
import json
import urllib2

def getStatistic(hostIP, statType, switchId='all'):
    if statType == 'LISTSW':
        url = 'http://{FLHostIP}:8080/wm/core/controller/switches/json'.format(FLHostIP=hostIP)
    elif statType == 'port':
        url = 'http://{FLHostIP}:8080/wm/core/switch/{swId}/{stat}/json'.format(FLHostIP=hostIP, swId=switchId, stat=statType)

    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        jsonResponse = json.loads(response.read())
        #print 'jsonResponse for '+ statType +': ' + str(jsonResponse)
        return jsonResponse
    except urllib2.HTTPError, e:
        raise e

def refreshSwitchList():
    swList = getStatistic(FloodLight.hostIP, 'LISTSW')
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

def updatePortStat(switchId):
    allPortStats = getStatistic(FloodLight.hostIP, 'port', switchId)[switchId]
    for port in allPortStats:
        currPort = Port.objects.filter(
                switch__dpid__exact = switchId,
                portNumber__exact = port['portNumber'],
                )[0]
        print currPort.hwAddr
        currPort.rcvdBytes = port['receiveBytes']
        currPort.save()

        #create new statistic


