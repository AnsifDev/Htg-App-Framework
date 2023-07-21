#!/bin/python3

import os
import site
import sys

site_locations = site.getsitepackages()
for site_location in site_locations:
    if site_location.startswith("/usr/lib"):
        install_loc = os.path.join(site_location, "Htg")
        break

remove = len(sys.argv[1:]) > 0 and sys.argv[1] == "remove"
install = len(sys.argv[1:]) > 0 and sys.argv[1] == "install"

def get_src_files(root: str = None):
    files = os.listdir(root)
    i = 0
    while(i < len(files)):
        if os.path.isdir(os.path.join(root if root else "", files[i])):
            folder = files.pop(i)
            if folder == "__pycache__": continue
            for file in os.listdir(os.path.join(root if root else "", folder)): 
                if file == "__pycache__": continue
                files.append(os.path.join(folder, file))
        else: i += 1
    return files

# for file in get_src_files(): print(file)
# exit(0)

if "--help" in sys.argv[1:]:
    print("Htg Library version 1.0")
    print("Htg [install/remove]\n\t- For installing and removing the library")

if remove: 
    if os.system("rm -r "+install_loc) != 0: print("Err: Uninstall failed"); exit(1)
    if os.system("rm /bin/Htg-app") != 0: print("Err: Uninstall failed"); exit(1)
    print("Uninstalled Htg Library")
elif install: 
    for file in get_src_files("Htg"): 
        if os.system("install -D "+os.path.join("Htg", file)+" "+os.path.join(install_loc, file)) != 0: print("Err: Install failed"); exit(1)
    if os.system("install -D Htg-app /bin/Htg-app") != 0: print("Err: Install failed"); exit(1)
    # if os.system("install -D setup.py "+os.path.join(install_loc, ".tools", "setup.py")) != 0: print("Err: Install failed"); exit(1)
    print("Installed Htg Library at", install_loc)
else: 
    print("Err: Operation unspecified\nPlease type ./setup.py --help for usage info")
    exit(2)