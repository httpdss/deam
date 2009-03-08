from os.path import join, abspath, dirname
from deam.utils.utils import directory_for_file

from deam.utils.repository_handler import RepositoryHandler
from deam.utils.wsgi_handler import WSGIHandler
from deam.utils.exceptions import NoAppsFileError

"""
TODO wsgi generator based on external.apps file location
TODO add libs support
TODO manage multiple subdirectories of a repository
TODO after app update, only copy if app has been updated
"""

DEFAULT_CONFIG = {}


class AppsManager(object):
    """
    This class represents
    """

    def __init__(self, base_path, config={}):
        """
        Constructor.
        """
        self.config = DEFAULT_CONFIG.update(config)

        self.app_folders = directory_for_file(base_path, 'external.apps')
        if not self.app_folders:
            raise NoAppsFileError('external.apps', base_path)

        #create all repository_handlers and store them in a list
        self.repositories = []
        for folder in self.app_folders:
            rh = RepositoryHandler(folder)
            rh.load_apps()
            self.repositories.append(rh)

    def download_app(self, app_name=''):
        """
        go for each folder that has the external.apps file and create
        the RepositoryHandler for it.
        """

        #TODO: check if app_name exists and throw error if it is not found
        #missing single app download implementation?
        
        for rh in self.repositories:
            rh.download_apps(app_name)

    def generate_wsgi(self, settings_path):
        """
        """
        wsgi_handler = WSGIHandler(self.app_folders)
        wsgi_handler.write_file('django.wsgi.tmp', settings_path)

    def list_external_apps(self):
        for rh in self.repositories:
            rh.list_apps()

if __name__ == '__main__':
    am = AppsManager(join(dirname(dirname(abspath(__file__))), 'testing'))
    am.download_app('basic')
