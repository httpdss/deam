import os, sys, subprocess, logging

from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.management.utils import get_project_root, directory_for_file
from subprocess import call

from deam.management.repository_handler import RepositoryHandler
from deam.management.wsgi_handler import WSGIHandler

#TODO alert the user to add the folders to the python path
#TODO wsgi generator based on external.apps file location
#TODO add libs support

APPS_FILE = 'external.apps'

class AppsManager(object):
    """
    This class represents
    """

    def __init__(self, base_path):
        """
        Constructor.
        """
        self.base_path = base_path
        self.app_folders = directory_for_file(self.base_path, APPS_FILE)

    def execute(self):
        """
        """
        for folder in self.app_folders:
            rh = RepositoryHandler(folder,APPS_FILE)
            rh.execute()

    def generate_wsgi(self, settings_path):
        """
        """
        wsgi_handler = WSGIHandler(self.app_folders)
        wsgi_handler.write_file('django.wsgi.tmp',settings_path)

def test_main():
    am = AppsManager('/home/kenny/testing/')
    am.generate_wsgi('papa')

if __name__ == '__main__':
    test_main()
