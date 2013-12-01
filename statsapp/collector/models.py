from django.db import models

class Switch(models.Model):
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
    hwAddr = models.TextField(null=True)
    #port number on switch
    portNumber = models.IntegerField(null=False)
    #connected to mac='xx.xx'  on the other side
    connectedTo = models.TextField(null=True)
    #receive bytes current value
    rcvdBytes = models.BigIntegerField(null=True)

class Statistic(models.Model):
    #aggr = aggregate( sum of all ports min(recvd bytes, transmit bytes) )
    #i dont collect any other stats for the time being, not reqd
    statisticType = models.TextField(null=False)
    #whole integer value, should wrap around
    value = models.BigIntegerField(null=True)
