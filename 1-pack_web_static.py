#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo."""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except:
        return None
