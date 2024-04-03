#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers,
using the function do_deploy."""

from fabric.api import env, put, run
import os


env.user = 'ubuntu'  # Assuming you're using the 'ubuntu' user
env.key_filename = ['/root/.ssh/school']  # Specify the path to your SSH private key

# Define the IP addresses of your web servers as strings
env.hosts = ['54.237.224.42', '3.80.18.166']

def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        basename = os.path.splitext(filename)[0]
        path_without_ext = "/data/web_static/releases/" + basename

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_without_ext))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_without_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}'.format(path_without_ext, path_without_ext))
        run('rm -rf {}/web_static'.format(path_without_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(path_without_ext))
        return True
    except Exception as e:
        return False
