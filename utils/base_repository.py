import os
import sys
from os.path import exists, join, abspath, dirname, lexists
from distutils.dir_util import copy_tree, remove_tree
import ConfigParser

class BaseRepository(object):
    """
    This class represents representation of external application
    """

    def __init__(self, val_dict):
        """
        Constructor.
        vcs_type -- type of the version control system. possible
                    values: svn, git and hg
        url -- url of repository
        folder -- project subfolder
        """

        #TODO validate format and throw exceptions
         #   if config.get(sec,'type') not in self.config['repos']:
         #       raise InvalidVCSTypeError(app['type'])
        self._vcs_type = val_dict['type']
        self._url = val_dict['url']
        self._name = val_dict['name']
        self._directory = val_dict['directory']
        self._location = val_dict['location']
        self._alert = val_dict.get('alert') or False

    def __cmp__(self, other):
        """compare by application name"""
        return cmp(self.name, other.name)

    def create(self):
        pass
    
    def update(self):
        pass
        
    def __unicode__(self):
        return "%s - %s" % (self._name, self._url)

    def get_absolute_directory(self):
        return join(self.location, self.directory)

    def is_created(self):
        return lexists(self.get_absolute_directory())

    def download_or_update(self):
        if self.is_created():
            self._repo_update()
        else:
            self._repo_create()

    def get_vcs_type(self):
        return self._vcs_type

    def set_vcs_type(self, vcs):
        self._vcs_type = vcs

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_directory(self):
        return self._directory

    def set_directory(self, directory):
        self._directory = directory

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def get_alert(self):
        return self._alert

    def set_alert(self, alert):
        self._alert = alert

    def show_alert(self):
        print "Remember to add this app to the python path."

    def _repo_create(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self._is_hidden_root_created():
            os.makedirs(self._get_hidden_root())

        #get the remote app from repository
        os.chdir(self._get_hidden_root())
        self.create()
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self._get_hidden_subfolder(), self.get_absolute_directory())

    def _repo_update(self):
        """
        Main function for repository update
        """

        #go to app hidden directory
        os.chdir(self._get_hidden_dir())
        #execute update command inside app directory
        self.update()
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self._get_hidden_subfolder(), self.get_absolute_directory(),update=1)

    def _get_hidden_subfolder(self):
        return join(self._get_hidden_dir(), self.directory)

    def _is_hidden_dir_created(self):
        return lexists(self._get_absolute_hidden_directory())

    def _get_hidden_dir(self):
        return join (self._get_hidden_root(), self.name)

    def _is_hidden_root_created(self):
        return lexists(self._get_hidden_root())

    def _get_hidden_root(self):
        """ get the repository directory depending on vcs type """
        hidden_dir = ".%s_repository" % self.vcs_type
        return join(self.location, hidden_dir)

    vcs_type = property(get_vcs_type, set_vcs_type)
    name = property(get_name, set_name)
    url = property(get_url, set_url)
    directory = property(get_directory, set_directory)
    location = property(get_location, set_location)
    alert = property(get_alert,set_alert)

if __name__ == '__main__':
    ea = ExternalApp({
        'name' : 'pepe',
        'url': 'http://django-command-extensions.googlecode.com/svn/trunk/',
        'type': 'svn',
        'directory' : 'django_extensions',
        'location' : '/home/kenny/testing/'
        })
    ea.download_or_update()
