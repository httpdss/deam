import os, sys, subprocess, logging

from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.utils.utils import get_project_root, directory_for_file
from deam.utils.external_app import ExternalApp
from subprocess import call

class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location, external_apps_file):
        """
        Constructor.
        """
        list.__init__(self)
        self.location = location
        self.external_apps_file = external_apps_file
        self.logger = logging.getLogger('repository_handler')
        self.logger.setLevel(logging.INFO)
        st = logging.StreamHandler()
        st.setLevel(logging.INFO)
        self.logger.addHandler(st)

    def show_alert(self):
        """
        """
        print "remember to add the apps to the python path"

    def download_apps(self):
        """
        """
        self.logger.info("Starting to download apps...")
        for app in self:
            lexists(join(self.location,app.name)) and self._repo_update(app) or self._repo_create(app)
        self.logger.info("Finished downloading apps")

    def _repo_create(self, app):
        """
        """
        os.chdir(self.location)
        if app.vcs_type == 'hg':
            call(['hg', 'clone', app.url, app.name])
        elif app.vcs_type == 'svn':
            call(['svn','co', app.url, app.name])
        elif app.vcs_type == 'git':
            call(['git', 'clone', app.url, app.name])
        else:
            print('%s has an invalid VCS system' % app.name)

    def _repo_update(self, app):
        """
        """
        os.chdir(join(self.location,app.name))
        if app.vcs_type == 'hg':
            call(['hg', 'pull', '-u'])
        elif app.vcs_type == 'svn':
            call(['svn','update'])
        elif app.vcs_type == 'git':
            call(['git', 'pull'])
        else:
            print('%s has an invalid VCS system' % app.name)

    def execute(self, do_download=True):
        """
        """
        apps_file_path = join(self.location,self.external_apps_file)
        if lexists(apps_file_path):
            infile = open(apps_file_path,'r')
            for line in infile:
                parts = line.split()
                self.append(ExternalApp(parts[0],parts[1],parts[2]))
            infile.close()
            if do_download:
                self.download_apps()
        else:
            print "File does not exist"
    def list_apps(self):
        print "%s:" % self.location
        for app in self:
            print "\t%s\t%s" % (app.name,app.url)

if __name__ == '__main__':
    rh = RepositoryHandler('/home/kenny/testing/a/','external.apps')
    rh.execute(False)
    rh.list_apps()

# vim: ai ts=4 sts=4 et sw=4
