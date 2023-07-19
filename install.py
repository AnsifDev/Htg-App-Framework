#!/bin/python3

import os
import sys

remove = len(sys.argv[1:]) > 0 and sys.argv[1] == "remove"
update = os.path.exists("/lib/python3/dist-packages/Htg")

if remove or update: 
    if os.system("rm -r /lib/python3/dist-packages/Htg") != 0: exit(1)
    if os.system("rm /bin/Htg-app") != 0: exit(1)

if not remove: 
    if os.system("cp -ru libhtg/Htg /lib/python3/dist-packages/Htg") != 0: exit(1)
    if os.system("cp libhtg/Htg-app /bin/Htg-app") != 0: exit(1)