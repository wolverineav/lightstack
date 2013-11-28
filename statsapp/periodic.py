import os
#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'statsapp'))
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'collector'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statsapp.settings")
#from django.core.management import *
from collector.tasks import *
import json
import pprint

def updateAll():
    refreshSwitchList()

if __name__ == "__main__":
    print 'running periodic task'
    updateAll()
    print 'complete'
