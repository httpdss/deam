import logging

from deam.utils.external_app import ExternalApp
from deam.utils.config_handler import ConfigHandler


class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location):
        """"
        Constructor.
        """
        self.location = location
        self.logger = logging.getLogger('repository_handler')
        self.logger.setLevel(logging.INFO)
        st = logging.StreamHandler()
        st.setLevel(logging.INFO)
        self.logger.addHandler(st)

    def download_apps(self, app_name=''):
        """
        """
        self.logger.info("Downloading apps...")
        for app in self:
            if app_name and app_name == app.name:
                app.download_or_update()
            elif not app_name:
                app.download_or_update()
        self.logger.info("Finished downloading apps")

    def load_apps(self):
        """ Parse the apps file and load each application to the list """
        cfg = ConfigHandler(self.location)
        for app_values in cfg.parse_apps_file():
            self.append(ExternalApp(app_values))

    def list_apps(self):
        print "%s:" % self.location
        for app in self:
            print "\t%s\t%s" % (app.name, app.url)

if __name__ == '__main__':
    from os.path import join, abspath, dirname
    deam_rel_root = dirname(dirname(abspath(__file__)))
    rh = RepositoryHandler(join(deam_rel_root, 'testing'))
    rh.execute(False)

# vim: ai ts=4 sts=4 et sw=4
