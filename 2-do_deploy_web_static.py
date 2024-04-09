#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers.

Execute: fab -f 1-deploy_web_static.py do_deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import put, run, env
from os.path import exists

# Replace with your web server IPs
env.hosts = ['52.91.149.144', '52.91.121.196']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
