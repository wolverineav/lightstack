# collector/api.py
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from collector.models import *

class SwitchResource(ModelResource):
    class Meta:
        queryset = Switch.objects.all()
        resource_name = 'switch'

class PortResource(ModelResource):
    switch = fields.ForeignKey(SwitchResource, 'switch')
    class Meta:
        queryset = Port.objects.all()
        resource_name = 'port'

class SwitchStatisticResource(ModelResource):
    switch = fields.ForeignKey(SwitchResource, 'switch')
    class Meta:
        queryset = SwitchStatistic.objects.all()
        resource_name = 'switchportaggr'
        ordering = ['timestamp']
