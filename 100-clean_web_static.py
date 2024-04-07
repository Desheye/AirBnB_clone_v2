#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives."""

from fabric.api import env, run, local, put
from os.path import exists
from datetime import datetime
from os import listdir

# Replace with your web server IPs
env.hosts = ['54.237.224.42', '3.80.18.166']
env.user = 'ubuntu'  # Replace with your SSH user
# Replace with the path to your SSH private key
env.key_filename = '/root/.ssh/your/school'


def do_clean(number=0):
    """Deletes out-of-date archives."""
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Clean local archives
        local(
            "ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number))

        # Clean remote archives
        releases_path = "/data/web_static/releases"
        archives = run(
            "ls -t {} | tail -n +{} || true".format(releases_path, number))
        if archives:
            archives = archives.split("\n")
            archives_to_delete = archives[number:]
            for archive in archives_to_delete:
                run("rm {}/{}".format(releases_path, archive))
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    do_clean()
