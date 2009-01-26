from django.conf import settings
from os.path import exists, join, abspath, dirname, lexists
import ConfigParser
import os

def get_config():
    config = {
        'apps_file': 'external.apps',
        'prefix': '.',
        'suffix': 'repo',
        'alert': True,
        'repos': { 
            'svn': 'svn',
            'hg': 'hg',
            'git': 'git',
        },
    }
    return config

def get_project_root():
    """ get the project root directory """
    settings_mod = __import__(settings.SETTINGS_MODULE, {}, {}, [''])
    return os.path.dirname(os.path.abspath(settings_mod.__file__))

def parse_apps_file(path_name):
    """parse an apps file """
    result = []
    config = ConfigParser.SafeConfigParser()
    config.read(path_name)
    for secs in config.sections():
        temp = { 
            'name': secs,
            'url': config.get(secs,'url'),
            'type': config.get(secs,'type'),
            'directory': config.get(secs,'directory'),
        }
        result.append(temp)
    return result

def directory_for_file(dir_name, file_name):
    '''
    '''
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            head,tail=os.path.split(dirfile)
            if tail == file_name:
                fileList.append(head)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile):
            fileList.extend(directory_for_file(dirfile,file_name))
    return fileList
# vim: ai ts=4 sts=4 et sw=4
