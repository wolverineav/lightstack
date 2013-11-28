from django.db import models

class Switch(models.Model):
    ''' leaf/spine? '''
    #type = vSwitch or pSwitch
    switchType = models.TextField(null=False)
    #switch's unique OF identifier
    dpid = models.TextField(null=False)
    #inet addr as available via OF
    inetAddr = models.TextField(null=False)

class Port(models.Model):
    #port belongs to
    switch = models.ForeignKey('Switch')
    #its MAC addr
    hwAddr = models.TextField(null=False)
    #port number on switch
    portNumber = models.IntegerField(null=False)
    #connected to mac='xx.xx'  on the other side
    connectedTo = models.TextField(null=True)

#class StatisticType(models.Model):
#    ''' port, queue, flow, aggregate, desc, table, features '''
#    name = models.TextField(null=False)

#class Statistic(models.Model):
#    statisticType = models.ForeignKey('StatisticType')
