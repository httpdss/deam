'''
Implementation of the application manager
'''

from os.path import join, abspath, dirname

from deam.utils.utils import directory_for_file
from deam.utils.repository_handler import RepositoryHandler
from deam.utils.wsgi_handler import WSGIHandler
from deam.utils.exceptions import NoAppsFileError


DEFAULT_CONFIG = {}


class AppsManager(object):
    """
    This class represents
    """

    def __init__(self, base_path, config = None):
        """
        Constructor.
        """
        if config:
            self.config = DEFAULT_CONFIG.update(config)

        self.app_folders = directory_for_file(base_path, 'external.apps')
        if not self.app_folders:
            raise NoAppsFileError('external.apps', base_path)

        #create all repository_handlers and store them in a list
        self.repositories = []
        for folder in self.app_folders:
            repo_handler = RepositoryHandler(folder)
            repo_handler.load_apps()
            self.repositories.append(repo_handler)

    def download_app(self, app_name = ''):
        """
        go for each folder that has the external.apps file and create
        the RepositoryHandler for it.
        """

        #TODO: check if app_name exists and throw error if it is not found
        #missing single app download implementation?

        for repo in self.repositories:
            repo.download_apps(app_name)

    def generate_wsgi(self, settings_path):
        """test function for wsgi autogeneration """
        wsgi_handler = WSGIHandler(self.app_folders)
        wsgi_handler.write_file('django.wsgi.tmp', settings_path)

    def list_external_apps(self):
        "list all external apps"
        for repo in self.repositories:
            repo.list_apps()

if __name__ == '__main__':
    AM = AppsManager(join(dirname(dirname(abspath(__file__))), 'testing'))
    AM.download_app('basic')
