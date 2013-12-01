from django.conf.urls import patterns, include, url
# REST API creation
from tastypie.api import Api
from collector.api import *

switchresource = SwitchResource()
portresource = PortResource()
switchstatresource = SwitchStatisticResource()

urlpatterns = patterns('',
    url(r'^api/', include(switchresource.urls)),
    url(r'^api/', include(portresource.urls)),
    url(r'^api/', include(switchstatresource.urls)),
    )
