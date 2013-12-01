# collector/api.py
from tastypie.resources import ModelResource
from collector.models import *

class SwitchResource(ModelResource):
    class Meta:
        queryset = Switch.objects.all()
        resource_name = 'switch'

class PortResource(ModelResource):
    class Meta:
        queryset = Port.objects.all()
        resource_name = 'port'

class SwitchStatisticResource(ModelResource):
    class Meta:
        queryset = SwitchStatistic.objects.all()
        resource_name = 'switchportaggr'
