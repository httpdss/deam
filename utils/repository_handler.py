import os, sys, subprocess, logging

from shutil import copytree, rmtree
from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.utils.utils import get_project_root, directory_for_file
from deam.utils.external_app import ExternalApp
from subprocess import call

REPO_DIRS = {'git': '.gitrepo',
             'hg': '.hgrepo',
             'svn': '.svnrepo',
}

"""
File structure
<application name> <repository url> <>
"""

class InvalidFormatError(Exception):
    pass

class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location, external_apps_file, repository_directories):
        """
        Constructor.
        """
        list.__init__(self)
        self.location = location
        self.external_apps_file = external_apps_file
        self.repository_directories = repository_directories
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
        self.logger.info("Downloading apps...")
        for app in self:
            print('Directory: %s' % app.directory)
            if lexists(join(self.location, app.directory)):
                self._repo_update(app)
            else:
                self._repo_create(app)
        self.logger.info("Finished downloading apps")

    def _repo_create_prepare(self, vcs_type):
        repo_dirs = join(self.location, self.repository_directories[vcs_type])
        if not lexists(repo_dirs):
            os.makedirs(repo_dirs)
        os.chdir(repo_dirs)

    def _repo_move(self, app):
        app_dir = join(self.location, app.directory)
        if lexists(app_dir):
            rmtree(app_dir)
        copytree(join(self.location, self.repository_directories[app.vcs_type], app.name, app.directory), app_dir)

    def _repo_create_call(self, app):
        if app.vcs_type == 'hg':
            call(['hg', 'clone', app.url, app.name])
        elif app.vcs_type == 'svn':
            call(['svn','co', app.url, app.name])
        elif app.vcs_type == 'git':
            call(['git', 'clone', app.url, app.name])

    def _repo_create(self, app):
        """
        """
        os.chdir(self.location)
        self._repo_create_prepare(app.vcs_type)
        self._repo_create_call(app)
        self._repo_move(app)

    def _repo_update_prepare(self, app):
        os.chdir(join(self.location, self.repository_directories[app.vcs_type], app.name))

    def _repo_update_call(self, vcs_type):
        if vcs_type == 'hg':
            call(['hg', 'pull', '-u'])
        if  vcs_type == 'svn':
            call(['svn','update'])
        elif vcs_type == 'git':
            call(['git', 'pull'])

    def _repo_update(self, app):
        """
        """
        self._repo_update_prepare(app)
        self._repo_update_call(app.vcs_type)
        self._repo_move(app)

    def execute(self, do_download=True):
        """
        """
        apps_file_path = join(self.location,self.external_apps_file)
        if lexists(apps_file_path):
            infile = open(apps_file_path,'r')
            for line in infile:
                parts = line.split()
                try:
                    self.append(ExternalApp(parts[0],parts[1],parts[2], parts[3]))
                except IndexError:#colocar el InvalidFormatError
                    print('%s format may be incorrect' % apps_file_path)
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
    rh = RepositoryHandler('/home/kenny/testing/a/','external.apps',REPO_DIRS)
    rh.execute(False)
    rh.list_apps()

# vim: ai ts=4 sts=4 et sw=4
