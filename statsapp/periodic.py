import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsapp.settings")
from collector.tasks import *
from collector.models import *
import json
import pprint

def updateAll():
    refreshSwitchList()
    sw = Switch.objects.all()
    updatePortStat(sw[0].dpid)

if __name__ == "__main__":
    print 'running periodic task'
    updateAll()
    print 'complete'
