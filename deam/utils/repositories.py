import os
from subprocess import call
from os.path import join, lexists
from distutils.dir_util import copy_tree
from deam.utils.utils import detect_type
from deam.utils.output import yellow

#TODO manage externals of svn repositories
#TODO manage git submodules

#TODO easy_install support (easy_install -d <destination_directory> <package_name>)

class BaseApplication(object):
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
        self._alert = val_dict.get('alert') or False
        self._directory = val_dict.get('directory') or ''
        self._location = val_dict['location']
        self._name = val_dict['name']
        self._url = val_dict['url']
        self._vcs_type = val_dict.get('type') or detect_type(val_dict.get('url'))

    def __cmp__(self, other):
        """compare by application name"""
        return cmp(self.name, other.name)

    def __unicode__(self):
        return "%s - %s" % (self._name, self._url)

    def get_absolute_directory(self):
        return join(self.location, self.directory or self.name)

    def is_created(self):
        return lexists(self.get_absolute_directory())

    def download_or_update(self):
        if self.is_created():
            print "Updating: %s" % yellow(self.name)
            self.update()
        else:
            print "Downloading: %s" % yellow(self.name)
            self.download()

    def show_alert(self):
        print "Remember to add this app to the python path."

    @property
    def vcs_type(self):
        return self._vcs_type

    @property
    def name(self):
        return self._name

    @property
    def directory(self):
        return self._directory

    @property
    def url(self):
        return self._url

    @property
    def location(self):
        return self._location

    @property
    def alert(self):
        return self._alert


class SvnApplication(BaseApplication):

    def update(self):
        """
        Main function for repository update
        """

        #go to app hidden directory
        os.chdir(self.__get_hidden_dir())
        #execute update command inside app directory
        call(['svn','update'])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory(), update=1)

    def download(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())

        #get the remote app from repository
        os.chdir(self.__get_hidden_root())
        call(['svn','co', self.url, self.name])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory())

    def get_constructor(values):
        return {'svn':SvnApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __is_hidden_dir_created(self):
        return lexists(self.__get_absolute_hidden_directory())

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        return join(self.location, '.svn_repository')

class GitApplication(BaseApplication):

    def download(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())

        #get the remote app from repository
        os.chdir(self.__get_hidden_root())
        call(['git', 'clone', self.url, self.name])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory())

    def update(self):
        """
        Main function for repository update
        """

        #go to app hidden directory
        os.chdir(self.__get_hidden_dir())
        #execute update command inside app directory
        call(['git', 'pull'])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory(),update=1)

    def get_constructor(values):
        return {'git':GitApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __is_hidden_dir_created(self):
        return lexists(self.__get_absolute_hidden_directory())

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        """ get the repository directory depending on vcs type """
        return join(self.location, '.git_repository')

class HgApplication(BaseApplication):

    def download(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())

        #get the remote app from repository
        os.chdir(self.__get_hidden_root())
        call(['hg', 'clone', self.url, self.name])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory())

    def update(self):
        """
        Main function for repository update
        """

        #go to app hidden directory
        os.chdir(self.__get_hidden_dir())
        #execute update command inside app directory
        call(['hg', 'pull', '-u'])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory(),update=1)

    def get_constructor(values):
        return {'hg':HgApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __is_hidden_dir_created(self):
        return lexists(self.__get_absolute_hidden_directory())

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        """ get the repository directory depending on vcs type """
        return join(self.location, '.hg_repository')

class SingleFileApplication(BaseApplication):
    #TODO create update function for SingleFileApplication
    #TODO SingleFileApplication need documentation

    def __init__(self, val_dict):
        BaseApplication.__init__(self,val_dict)
        self.__filename = val_dict.get('filename')

    @property
    def filename(self):
        return self.__filename

    def download(self):
        """
        Main function for repository create
        """
        import urllib
        urllib.urlretrieve(self.url, join(self.location, self.filename))

    def update(self):
        print "Updating is not supported on single files"

    def get_constructor(values):
        return {'file':SingleFileApplication(values)}

    def is_created(self):
        return lexists(join(self.location,self.filename))

if __name__ == '__main__':
    ea = SingleFileApplication({
        'name' : 'pepe',
        'url': 'http://www.djangosnippets.org/snippets/1135/download/',
        'filename': 'firebug.py',
        'type': 'file',
        'location' : '/home/kenny/'
        })
    ea.download_or_update()
