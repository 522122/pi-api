import sys

#activate_this = '/media/SSD/data/WWW/pi-api/venv/bin/activate'
#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0, '/media/SSD/data/WWW/pi-api')
from main import app as application