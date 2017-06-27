from google.appengine.ext import vendor
import os
import sys

vendor.add('lib')

if os.name == 'nt':
    os.name = None
    sys.platform = ''
