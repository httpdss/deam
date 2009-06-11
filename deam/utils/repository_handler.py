import logging

from deam.utils.config_handler import ConfigHandler
from deam.utils.repositories import GitApplication, SvnApplication, HgApplication, SingleFileApplication
from deam.utils.utils import detect_type, TermColors
from deam.utils.output import yellow
from Queue import Queue
from threading import Thread, Lock


#TODO: cant do without locks, switch to fork()?

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

    def worker(self, q, lo):
        while True:
            app = q.get()
            lo.acquire()
            try:
                app.download_or_update()
            finally:
                lo.release()
            q.task_done()

    def download_apps(self, app_name=''):
        """
        """
        q = Queue()
        lo = Lock()
        print 'Preparing for download/update'
        for i in range(2):
            current = Thread(target=self.worker, args=(q,lo,))
            current.setDaemon(True)
            current.start()
        for app in self:
            if (app_name and app_name == app.name) or not app_name:
                q.put(app)
        q.join()
        print 'Download/update complete'
        for app in self:
            if app.has_patch():
                print "\nDisplaying %s patch\n\n" % yellow(app.name)
                app.display_patch()
                option = raw_input("\nWould you like to apply this patch? (Y/n) ")
                if option in ['Y', 'y', '']:
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
        print "%s%s:%s" % (TermColors.HEADER,self.location,TermColors.ENDC)
        for app in self:
            print "\t%s%s%s\t%s" % (TermColors.YELLOW,app.name,TermColors.ENDC, app.url)

if __name__ == '__main__':
    from os.path import join, abspath, dirname
    deam_rel_root = dirname(dirname(abspath(__file__)))
    rh = RepositoryHandler(join(deam_rel_root, 'testing'))
    rh.execute(False)

# vim: ai ts=4 sts=4 et sw=4
