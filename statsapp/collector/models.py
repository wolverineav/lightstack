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
    #store the sum and delta
    aggr = models.BigIntegerField(default = 0)
    delta = models.BigIntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class SwitchStatistic(Statistic):
    switch = models.ForeignKey(Switch)
