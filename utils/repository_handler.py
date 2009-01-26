import os
import sys
import subprocess
import logging

from shutil import copytree, rmtree
from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.utils.utils import get_project_root, directory_for_file, \
get_config, parse_apps_file
from deam.utils.external_app import ExternalApp
from deam.utils.exceptions import InvalidVCSTypeError, NoAppFound
from subprocess import call

class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location, config={}):
        """"
        Constructor.
        """
        configdef = get_config()
        for k in config:
            configdef[k] = config[k]
        self.config = configdef
        self.apps = []
        self.location = location
        self.logger = logging.getLogger('repository_handler')
        self.logger.setLevel(logging.INFO)
        st = logging.StreamHandler()
        st.setLevel(logging.INFO)
        self.logger.addHandler(st)

    def show_alert(self):
        """
        """
        print "Remember to add this app to the python path."

    def download_apps(self):
        """
        """
        self.logger.info("Downloading apps...")
        for app in self.apps:
            if lexists(join(self.location, app.directory)):
                self._repo_update(app)
            else:
                self._repo_create(app)
                if self.config['alert']:
                    self.show_alert()
        self.logger.info("Finished downloading apps")

    def _repo_create_prepare(self, vcs_type):
        repo_dir = join(self.location, self._get_repo_dir(vcs_type))
        if not lexists(repo_dir):
            os.makedirs(repo_dir)
        os.chdir(repo_dir)

    def _repo_move(self, app):
        repo_dir = self._get_repo_dir(app.vcs_type) 
        app_dir = join(self.location, app.directory)
        if lexists(app_dir): 
            rmtree(app_dir)
        copytree(join(self.location, repo_dir, app.name, app.directory), \
        app_dir)

    def _repo_create_call(self, app):
        if app.vcs_type == self.config['repos']['hg']:
            call(['hg', 'clone', app.url, app.name])
        elif app.vcs_type == self.config['repos']['svn']:
            call(['svn','co', app.url, app.name])
        elif app.vcs_type == self.config['repos']['git']:
            call(['git', 'clone', app.url, app.name])

    def _repo_create(self, app):
        """
        """
        os.chdir(self.location)
        self._repo_create_prepare(app.vcs_type)
        self._repo_create_call(app)
        self._repo_move(app)

    def _get_repo_dir(self, vcs_type):
        return self.config['prefix'] + vcs_type + self.config['suffix']


    def _repo_update_prepare(self, app):
        repo_dir = self._get_repo_dir(app.vcs_type)
        os.chdir(join(self.location, repo_dir, app.name))

    def _repo_update_call(self, vcs_type):
        if vcs_type == self.config['repos']['hg']:
            call(['hg', 'pull', '-u'])
        if vcs_type == self.config['repos']['svn']:
            call(['svn','update'])
        elif vcs_type == self.config['repos']['git']:
            call(['git', 'pull'])

    def _repo_update(self, app):
        """
        """
        self._repo_update_prepare(app)
        self._repo_update_call(app.vcs_type)
        self._repo_move(app)

    def _add_external_app(self, v):
        """docstring for _add_external_app"""
        self.apps.append(ExternalApp(v))

    def execute(self, do_download=True):
        """
        """
        apps_file_path = join(self.location,self.config['apps_file'])
        parse = parse_apps_file(apps_file_path)
        single_found = False
        for v in parse:
            if v['type'] not in self.config['repos']:
                raise InvalidVCSTypeError(v['type'])
            if self.config['single'] != None and v['name'] == \
            self.config['single']:
                self._add_external_app(v)
                single_found = True
                break
            elif self.config['single'] == None:
                self._add_external_app(v)
        if self.config['single'] != None and not single_found:
            raise NoAppFound(self.config['single'])
        if do_download:
            self.download_apps()
        
    def list_apps(self):
        print "%s:" % self.location
        for app in self:
            print "\t%s\t%s" % (app.name,app.url)


if __name__ == '__main__':
    deam_rel_root = dirname(dirname(abspath(__file__)))
    rh = RepositoryHandler(join(deam_rel_root, 'testing'))
    rh.execute(False)
    rh.list_apps()

# vim: ai ts=4 sts=4 et sw=4
