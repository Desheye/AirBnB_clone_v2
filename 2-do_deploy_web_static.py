#!/usr/bin/python3
# This Fabfile is used to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["54.237.224.42", "3.80.18.166"]


def do_deploy(archive_path):
    """Distribute an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: Returns False if the file doesn't exist at archive_path or an error occurs, otherwise True.
    """
    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False
    if run("rm /tmp/{}".format(file)).failed:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False
    return True
