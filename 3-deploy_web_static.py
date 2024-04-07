#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers."""

from fabric.api import env, run, local, put
from os.path import exists
from datetime import datetime

env.hosts = ['54.237.224.42', '3.80.18.166']  # Replace with your web server IPs
env.user = 'ubuntu'  # Replace with your SSH user


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        if exists(archive_path):
            return archive_path
        else:
            return None
    except Exception as e:
        print(e)
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not archive_path:
        return False
    try:
        filename = archive_path.split("/")[-1]
        path_without_ext = "/data/web_static/releases/{}/".format(filename.split(".")[0])

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_without_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_without_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_without_ext, path_without_ext))
        run("rm -rf {}web_static".format(path_without_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_without_ext))
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """Deploys the web_static folder to your web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()
