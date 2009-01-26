class Error(Exception):
    pass

class InvalidVCSTypeError(Error):
    def __init__(self, vcstype):
        self.vcstype = vcstype
    def __str__(self):
        return repr('%s not found in configuration.' % self.vcstype)

class NoAppsFileError(Error):
    def __init__(self, appfile, basedir):
        self.appfile = appfile
        self.basedir = basedir
    def __str__(self):
        return repr('Could not find %s inside %s subdirectories.' % \
        (self.appfile, self.basedir)) 

        