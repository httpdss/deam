"""
repository handler

"""
import logging

from deam.utils.config_handler import ConfigHandler
from deam.utils.repositories import GitApplication, SvnApplication, \
    HgApplication, SingleFileApplication
from deam.utils.utils import detect_type, TermColors
from deam.utils.output import yellow
from Queue import Queue
from threading import Thread


#TODO: cant do without locks, switch to fork()? #IGNORE:W0511

class RepositoryHandler(list):
    """
    This class represents the manager of external apps
    """

    def __init__(self, location):
        """"
        Constructor.
        """
        list.__init__(self)
        self.location = location
        self.logger = logging.getLogger('repository_handler')
        self.logger.setLevel(logging.INFO)
        strm = logging.StreamHandler()
        strm.setLevel(logging.INFO)
        self.logger.addHandler(strm)

    def download_thread(self, queue):
        """worker method thread that does the downloading"""
        while True:
            app = queue.get()
            app.download_or_update()
            queue.task_done()

    def download_apps(self, app_name = ''):
        """
        download one or multiple apps in threaded mode
        """
        queue = Queue()
        self.logger.info('Preparing for download/update')
        for i in range(2):
            current = Thread(target = self.download_thread, name = "dl-%s" % i, args = (queue,))
            current.setDaemon(True)
            current.start()
        for app in self:
            if (app_name and app_name == app.name) or not app_name:
                queue.put(app)
        queue.join()
        self.logger.info('Download/update complete')
        for app in self:
            if app.has_patch():
                print "\nDisplaying %s patch\n\n" % yellow(app.name)
                app.display_patch()
                option = raw_input("\nWould you like to apply this patch? (y/N) ")
                if option.lower()  == 'y':
                    app.apply_patch()

    def load_apps(self):
        """ Parse the apps file and load each application to the list """
        cfg = ConfigHandler(self.location)
        for app_values in cfg.parse_apps_file():
            app_type = app_values.get('type') or detect_type(app_values.get('url'))
            repo = {'hg' : HgApplication(app_values),
                    'svn' : SvnApplication(app_values),
                    'git' : GitApplication(app_values),
                    'file' : SingleFileApplication(app_values),
                    None : None,
                    }[app_type]
            self.append(repo)

    def list_apps(self):
        print "%s%s:%s" % (TermColors.HEADER, self.location, TermColors.ENDC)
        for app in self:
            print "\t%s%s%s\t%s" % (TermColors.YELLOW, app.name, TermColors.ENDC, app.url)

