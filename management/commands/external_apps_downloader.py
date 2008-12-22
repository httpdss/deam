#!/usr/bin/python

#TODO apps file in folder search.

import os, sys, subprocess, logging
import pysvn
import optparse

from os.path import exists, join
from os import pathsep
from string import split
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


APPS_FILE = 'external.apps'

def search_file(filename, search_path):
   """Given a search path, find file
   """
   file_found = 0
   paths = string.split(search_path, pathsep)
   for path in paths:
      if exists(join(path, filename)):
          file_found = 1
          break
   if file_found:
      return True
   else:
      return False

class ExternalApp(object):
    """
    This class represents representation of external application
    """

    def __init__(self,name, url, vcs_type = 'svn'):
        """
        Constructor.
        
        vcs_type -- type of the version control system. possible 
                    values: svn, git and hg
        url -- url of repository
        """
        self._vcs_type = vcs_type
        self._url = url
        self._name = name

    def get_vcs_type(self):
        return self._vcs_type

    def set_vcs_type(self, vcs):
        self._vcs_type = vcs

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    vcs_type = property(get_vcs_type, set_vcs_type)
    name = property(get_name, set_name)
    url = property(get_url, set_url)

class AppManager(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location):
        """
        Constructor.
        """
        list.__init__(self)
        self.location = location

    def download_apps(self):
        """
        
        """
        logging.debug("Starting to download apps...")

        for app in self:
            vcs_type = app.vcs_type
            if (vcs_type == 'svn'):
                self._download_from_svn(app)
            elif (vcs_type == 'git'):
                self._download_from_git(app)
            else:
                self._download_from_mercurial(app)

        logging.debug("Finished downloading apps")

    def _download_from_svn(self,app):
        """
        svn checkout method for the selected application
        
        
        app -- an ExternalApp object of type svn
        """
        assert app.vcs_type == 'svn'
        logging.debug("Checking out %s" % app.name)
        client = pysvn.Client()
        client.checkout(app.url,"%s/%s" % (self.location,app.name))
        logging.debug("Checkout completed")

    def _download_from_git(self,app):
        """
        
        
        app -- an ExternalApp object of type git 
        """
        assert app.vcs_type == 'git'

    def _download_from_mercurial(self,app):
        """
        
        
        app -- an ExternalApp object of type hg 
        """
        assert app.vcs_type == 'hg'

    #def _external_file_search(self):
    #    """
    #    find all external apps file within a directory only depth 1
    #    """
    #    dir_list = []
    #    for directory in os.listdir(self.location)[1:]:
    #        file_found = search_file(APPS_FILE, os.path.join(self.location,directory))
    #        if file_found:
    #            dir_list.append(os.path.join(self.location,directory, APPS_FILE))
    #    return dir_list

    #def execute(self):
    #    """
    #    append all external apps to list structure.
    #    """
    #    app_files = self._external_file_search()
    #    for app_file in app_files:
    #        infile = open(app_file,'r')
    #        for line in infile:
    #            parts = line.split()
    #            self.append(ExternalApp(parts[0],parts[1],parts[2]))
    #        infile.close()
    #        self._download_apps()
    #        self = []
    def execute(self):
        """
        
        """
        apps_file_path = os.path.join(self.location,APPS_FILE)
        if os.path.exists(apps_file_path):
            infile = open(apps_file_path,'r')
            for line in infile:
                parts = line.split()
                self.append(ExternalApp(parts[0],parts[1],parts[2]))
            infile.close()
            self.download_apps()
        else:
            print "File does not exist"

class Command(BaseCommand):

    help = 'Download all external apps defined for your django project'

    def handle(self, *args, **options):
        """
        external apps command handler
        """
        if not hasattr(settings, 'EXTERNAL_APPS_FOLDER'):
            raise CommandError('External apps folder missing in settings.py. Please define the external apps directory with EXTERNAL_APPS_FOLDER')
        self.app_manager = AppManager(settings.EXTERNAL_APPS_FOLDER)
        self.app_manager.execute()

def main():
    app_manager = AppManager(EXTERNAL_APPS_PATH)
    app_manager.execute()

if __name__ == '__main__':
    main()

# vim: ai ts=4 sts=4 et sw=4
