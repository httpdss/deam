import os, sys, subprocess, logging

from os.path import exists, join, abspath, dirname, lexists
from os import pathsep
from string import split
from deam.management.utils import get_project_root, directory_for_file
from subprocess import call

#TODO alert the user to add the folders to the python path
#TODO wsgi generator based on external.apps file location
#

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
            if lexists(join(self.location,app.name)):
                self.logger.info("Updating %s" % app.name)
                self._repo_update(app)
                self.logger.debug("Update completed")
            else: 
                self.logger.info("Downloading %s" % app.name)
                self._repo_create(app)
                self.logger.debug("Download completed")
        self.logger.info("Finished downloading apps")

    def _repo_create(self,app):
        os.chdir("%s" % self.location)
        if app.vcs_type == 'hg':
            call(['hg', 'clone', '%s' % app.url, '%s' % app.name])
        elif app.vcs_type == 'svn':
            call(['svn','co', '%s' % app.url, '%s' % app.name])
        elif app.vcs_type == 'git':
            call(['git', 'clone', '%s' % app.url, '%s' % app.name])
        else:
            print('%s has an invalid VCS system' % app.name)
            
    def _repo_update(self,app):
        os.chdir(join(self.location,app.name))
        if app.vcs_type == 'hg':
            call(['hg', 'pull', '-u'])
        elif app.vcs_type == 'svn':
            call(['svn','update'])
        elif app.vcs_type == 'git':
            call(['git', 'pull'])
        else:
            print('%s has an invalid VCS system' % app.name)
        
    def execute(self):
        """
        """
        apps_file_path = join(self.location,APPS_FILE)
        if lexists(apps_file_path):
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

    def generate_wsgi(self, settings_path):
        """
        
        """
        #TODO add libs support
        wsgi_file = open('django.wsgi.tmp','w')
        wsgi_file.writelines([
            'import os\n',
            'import sys\n'
            'sys.stdout = sys.stderr\n'
            'from os.path import abspath, dirname, join\n',
            'from site import addsitedir\n',
            'path = addsitedir(abspath(join(dirname(__file__), \'django-hotclub\', \'external_libs\')), set())\n',
            'if path: sys.path = list(path) + sys.path\n'])

        #add all folders to python path
        for folder in self.app_folders:
            wsgi_file.write( 'sys.path.insert(0, abspath(\'%s\'))\n' % folder)

        wsgi_file.writelines([
            '\n',
            'from django.core.handlers.wsgi import WSGIHandler\n',
            '\n',
            'os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'%s\'\n' % settings_path,
            '\n',
            'application = WSGIHandler()\n' ])

def test_main():
    am = AppsManager(join(dirname(abspath(__file__)),'..','testing'))
    am.execute()

if __name__ == '__main__':
    test_main()
