import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cogitoXInfor.settings')
django.setup()

import csv
from GoogleAmazone.models import Recommendations, Products

# Add a recommendation calculation here to precompile recommendations 
# and add then to the database in the Recommendations table

