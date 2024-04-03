<<<<<<< HEAD
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
=======
#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
>>>>>>> 5ad838c611b22b1a462175ca002bcaaa1f0f54e3
