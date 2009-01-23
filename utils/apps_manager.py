import os
import sys
import subprocess
import logging

from deam.utils.exceptions import DeamError
from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.utils.utils import get_project_root, directory_for_file, get_config
from subprocess import call

from deam.utils.repository_handler import RepositoryHandler
from deam.utils.wsgi_handler import WSGIHandler

"""
TODO alert the user to add the folders to the python path
TODO wsgi generator based on external.apps file location
TODO add libs support
external.apps test location is 1 in utils/../testing (utils is where
apps_manager.py is)
TODO manage multiple subdirectories of a repository
TODO single app download/update
"""

class AppsManager(object):
    """
    This class represents
    """
    def __init__(self, base_path, config={}):
        """
        Constructor.
        """

        self.base_path = base_path
        self.config_path = dirname(dirname(abspath(__file__)))
        self.config = get_config()
        for k in config:
            self.config[k] = config[k]
        self.app_folders = directory_for_file(self.base_path, \
        self.config['apps_file'])
        if self.app_folders == []:
            raise DeamError("Could not find %s in the base path %s" % \
            (self.config['apps_file'], self.base_path))
        
    def execute(self):
        """
        """
        for folder in self.app_folders:
            rh = RepositoryHandler(folder, self.config)
            rh.execute()

    def generate_wsgi(self, settings_path):
        """
        """
        wsgi_handler = WSGIHandler(self.app_folders)
        wsgi_handler.write_file('django.wsgi.tmp', settings_path)

    def list_external_apps(self):
        for folder in self.app_folders:
            rh = RepositoryHandler(folder,self.config)
            rh.execute(False)
            rh.list_apps()

def test_main():
    am = AppsManager(join(dirname(dirname(abspath(__file__))), 'testing'))
    am.execute()
    am.list_external_apps()
    
if __name__ == '__main__':
    test_main()
