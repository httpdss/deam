import os, sys, subprocess, logging
import pysvn

from os.path import exists, join
from os import pathsep
from string import split
from external_downloads.management.utils import get_project_root, directory_for_file

#TODO alert the user to add the folders to the python path

APPS_FILE = 'external.apps'

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

class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location):
        """
        Constructor.
        """
        list.__init__(self)
        self.location = location

    def show_alert(self):
        """
        """
        print "remember to add the apps to the python path"

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
            rh = RepositoryHandler(folder)
            rh.execute()

def test_main():
    am = AppsManager('/home/kenny/testing')
    am.execute()

if __name__ == '__main__':
    test_main()

# vim: ai ts=4 sts=4 et sw=4
