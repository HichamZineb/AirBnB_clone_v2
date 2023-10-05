#!/usr/bin/python3
"""Distributes an archive to your web servers using the function do_deploy."""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['35.153.231.121', '54.236.24.144']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        file_name = archive_path.split('/')[-1]
        folder_name = file_name.replace('.tgz', '')
        release_path = '/data/web_static/releases/' + folder_name
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))

        run('rm /tmp/{}'.format(file_name))

        run('mv {}/web_static/* {}'.format(release_path, release_path))

        run('rm -rf {}/web_static'.format(release_path))

        # Update the symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))

        print('New version deployed!')
        return True

    except Exception as e:
        print(str(e))
        return False
