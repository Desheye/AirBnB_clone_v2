#!/usr/bin/python3
"""
Deletes outdated archives.

Usage:
fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

# Define the host(s)
env.hosts = ['52.91.149.144', '52.91.121.196']

def do_clean(number=0):
    """
    Delete outdated archives.

    Args:
        number (int): Number of archives to keep. If set to 0 or 1, keeps only the
                      most recent archive. If set to 2, keeps the two most recent archives,
                      and so on.
    """
    # Ensure number is an integer
    number = 1 if int(number) == 0 else int(number)

    # Delete local outdated archives
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Delete remote outdated archives
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
