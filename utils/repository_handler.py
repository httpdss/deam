import os
import sys
import subprocess
import logging

from xml.dom import minidom
from shutil import copytree, rmtree
from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.utils.utils import get_project_root, directory_for_file, get_config
from deam.utils.external_app import ExternalApp
from deam.utils.exceptions import IncorrectFormatError
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
        self.location = location
        self.external_apps_file = configdef['apps_file']
        self.repos = configdef['repos']
        self.repo_dir_prefix = configdef['prefix']
        self.repo_dir_suffix = configdef['suffix']
        self.alert = configdef['alert']
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
        for app in self:
            if lexists(join(self.location, app.directory)):
                self._repo_update(app)
            else:
                self._repo_create(app)
                if self.alert:
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
        copytree(join(self.location, repo_dir, app.name, app.directory),app_dir)

    def _repo_create_call(self, app):
        if app.vcs_type == self.repos['hg']:
            call(['hg', 'clone', app.url, app.name])
        elif app.vcs_type == self.repos['svn']:
            call(['svn','co', app.url, app.name])
        elif app.vcs_type == self.repos['git']:
            call(['git', 'clone', app.url, app.name])

    def _repo_create(self, app):
        """
        """
        os.chdir(self.location)
        self._repo_create_prepare(app.vcs_type)
        self._repo_create_call(app)
        self._repo_move(app)

    def _get_repo_dir(self, vcs_type):
        return self.repo_dir_prefix + vcs_type + self.repo_dir_suffix


    def _repo_update_prepare(self, app):
        repo_dir = self._get_repo_dir(app.vcs_type)
        os.chdir(join(self.location, repo_dir, app.name))

    def _repo_update_call(self, vcs_type):
        if vcs_type == self.repos['hg']:
            call(['hg', 'pull', '-u'])
        if vcs_type == self.repos['svn']:
            call(['svn','update'])
        elif vcs_type == self.repos['git']:
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
        #if lexists(apps_file_path):
        xmldoc = minidom.parse(apps_file_path)
        name_list = xmldoc.getElementsByTagName('name')
        url_list = xmldoc.getElementsByTagName('url')
        repo_type_list = xmldoc.getElementsByTagName('type')
        directory_list = xmldoc.getElementsByTagName('directory')
        if not (len(name_list) == len(url_list) == len(repo_type_list) \
        == len(directory_list)):
            raise IncorrectFormatError(apps_file_path)
        for i, v in enumerate(name_list):
            self.append(ExternalApp(name_list[i].childNodes[0].nodeValue, \
            url_list[i].childNodes[0].nodeValue, \
            repo_type_list[i].childNodes[0].nodeValue, \
            directory_list[i].childNodes[0].nodeValue))
        if do_download:
            self.download_apps()
        
    def list_apps(self):
        print "%s:" % self.location
        for app in self:
            print "\t%s\t%s" % (app.name,app.url)


if __name__ == '__main__':
    deam_rel_root = dirname(dirname(abspath(__file__)))
    rh = RepositoryHandler(join(deam_rel_root, 'testing'), deam_rel_root)
    rh.execute(False)
    rh.list_apps()

# vim: ai ts=4 sts=4 et sw=4
