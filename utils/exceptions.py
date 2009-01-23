class Error(Exception):
    pass

class IncorrectFormatError(Error):
    pass

class NoAppsFileError(Error):
    def __init__(self, appfile, basedir):
        self.appfile = appfile
        self.basedir = basedir
    def __str__(self):
        return repr('Could not find %s inside %s subdirectories.' % \
        (self.appfile, self.basedir)) 

        