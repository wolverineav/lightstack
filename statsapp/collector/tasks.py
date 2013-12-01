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
            #create stats as well
            SwitchStatistic.objects.create(switch = new_sw)
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
    currSwitch = Switch.objects.get(dpid__exact = switchId)
    swPorts = Port.objects.filter(switch__dpid__exact = switchId)
    newAggr = 0
    for port in allPortStats:
        newAggr = newAggr + port['receiveBytes']
        currPort = swPorts.filter(portNumber__exact = port['portNumber'])[0]
        currPort.rcvdBytes = port['receiveBytes']
        currPort.save()

    #create new statistic
    oldStat = SwitchStatistic.objects.filter(switch__dpid__exact = switchId).order_by('-timestamp')[0]
    if newAggr != oldStat.aggr:
        newStat = SwitchStatistic.objects.create(switch = currSwitch)
        newStat.aggr = newAggr
        if newAggr < oldStat.aggr: #some field flipped, turn around
            newStat.delta = (2147483647 - oldStat.aggr) + newAggr
        else:
            newStat.delta = newAggr - oldStat.aggr
        newStat.save()
