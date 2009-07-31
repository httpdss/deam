import os
import re
from subprocess import PIPE, call, Popen
from os.path import join, lexists
from urllib import urlretrieve
from distutils.dir_util import copy_tree

from deam.utils.utils import detect_type, output_to_file, output_file
from deam.utils.utils import get_patch_directory


#TODO: manage externals of svn repositories
#TODO: manage git submodules
#TODO: delete patch after selecting yes to apply
#TODO: easy_install support (easy_install -d <destination_directory> <package_name>)
#TODO: update support for mercurial

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
        self._vcs_type = detect_type(val_dict.get('url'), \
                                     default = val_dict.get('type'))

    def __cmp__(self, other):
        """compare by application name"""
        return cmp(self.name, other.name)

    def __unicode__(self):
        return "%s - %s" % (self._name, self._url)

    def get_absolute_directory(self):
        """get the absolute directory path to the application"""
        return join(self.location, self.directory or self.name or '')

    def is_created(self):
        """check if application exists"""
        return lexists(self.get_absolute_directory())

    def display_patch(self):
        """show patch"""
        output_file(self.name)

    def has_patch(self):
        """check if a patch exists for this application"""
        return os.path.isfile(os.path.join(get_patch_directory(), self.name))

    def download_or_update(self):
        """check if download or update is needed"""
        if self.is_created():
            self.update()
        else:
            self.download()

    @staticmethod
    def show_alert():
        """"shows alert on install"""
        print "Remember to add this app to the python path."

    def update(self):
        """update method"""
        raise NotImplementedError

    def download(self):
        """download method"""
        raise NotImplementedError

    @property
    def vcs_type(self):
        """type of version control system"""
        return self._vcs_type

    @property
    def name(self):
        """name of application"""

        return self._name

    @property
    def directory(self):
        """directory path of application"""
        return self._directory

    @property
    def url(self):
        """source url for downloading the application"""
        return self._url

    @property
    def location(self):
        """location of application folder"""
        return self._location

    @property
    def alert(self):
        """if set true it will alert user on update"""
        return self._alert


class SvnApplication(BaseApplication):
    """SVN specific functions for applications"""

    def update(self):
        """
        Main function for repository update
        """
        #go to app hidden directory
        #execute update command inside app directory
        revision = Popen(['svn', 'info', self.__get_hidden_dir()], \
                         stdout = PIPE).communicate()[0]
        oldrev = self.get_revision(revision)
        #TODO: could this be a call to subprocess.call ?
        Popen(['svn', 'update', self.__get_hidden_dir()], \
              stdout = PIPE).communicate()[0]
        #copy the desired subfolder from hidden to the app directory
        revision = Popen(['svn', 'info', self.__get_hidden_dir()], \
                         stdout = PIPE).communicate()[0]
        newrev = self.get_revision(revision)
        rev_range = oldrev + ':' + newrev
        output = Popen(['svn', 'diff', self.__get_hidden_dir(), \
                        '-r', rev_range, self.directory], \
                        stdout = PIPE).communicate()[0]
        output_to_file(output, self.name)

    def patch_directory(self):
        return os.path.join(get_patch_directory(), self.name)

    def apply_patch(self):
        """apply the patch located in the patch directory"""
        os.chdir(self.get_absolute_directory())
        patch_process = Popen(['patch', '-p1', '-i', \
                               self.patch_directory()]).communicate()


    def download(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())
        #get the remote app from repository
        call(['svn', 'co', self.url, self.__get_hidden_dir()])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory())

    def get_constructor(self, values):
        return {'svn':SvnApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        return join(self.location, '.svn_repository')

    def get_revision(self, revision):
        m = re.search('Revision: (\d+)', revision)
        if m:
            return str(m.group(1))
        return "-1"

class GitApplication(BaseApplication):

    def download(self):
        """
        Main function for repository create
        """
        #create the hidden root
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())
        #get the remote app from repository
        call(['git', 'clone', self.url, self.__get_hidden_dir()])
        #copy the desired subfolder from hidden to the app directory
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory())

    def apply_patch(self):
        os.chdir(self.get_absolute_directory())
        p3 = Popen(['patch', '-p2', '-i', os.path.join(get_patch_directory(), self.name)]).communicate()

    def update(self):
        """
        Main function for repository update
        """
        #go to app hidden directory
        #execute update command inside app directory
        #grab which is the current version
        oldhash = Popen(['git', '--git-dir=' + os.path.join(self.__get_hidden_dir(), '.git'), '--no-pager', 'log', '--pretty=format:%H', '-1'], stdout = PIPE).communicate()[0]
        #git --no-pager log --pretty=format:%H -1
        Popen(['git', '--git-dir=' + os.path.join(self.__get_hidden_dir(), '.git'), 'pull'], stdout = PIPE).communicate()[0]
        #diff old hash againt HEAD
        #copy the desired subfolder from hidden to the app directory
        output = Popen(['git', '--git-dir=' + os.path.join(self.__get_hidden_dir(), '.git'), '--no-pager', 'diff', oldhash, 'HEAD'], stdout = PIPE).communicate()[0]
        output_to_file(output, self.name)


    def get_constructor(self, values):
        return {'git':GitApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        """ get the repository directory depending on vcs type """
        return join(self.location, '.git_repository')

class HgApplication(BaseApplication):

    def apply_patch(self):
        pass

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
        copy_tree(self.__get_hidden_subfolder(), self.get_absolute_directory(), update = 1)

    def get_constructor(self, values):
        return {'hg':HgApplication(values)}

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

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
        BaseApplication.__init__(self, val_dict)
        self.__filename = val_dict.get('filename')

    @property
    def filename(self):
        return self.__filename

    def download(self):
        """
        Main function for repository create
        """
        if not self.__is_hidden_root_created():
            os.makedirs(self.__get_hidden_root())
        urlretrieve(self.url, join(self.location, self.filename))

    def apply_patch(self):
        os.chdir(self.location)
        p3 = Popen(['patch', self.filename, join(get_patch_directory(), self.name)]).communicate()

    def update(self):
        urlretrieve(self.url, join(self.location, self.filename + '.tmp'))
        #strip_rn(join(self.location, self.filename + '.tmp'))
        #strip_rn(join(self.location, self.filename))
        output = Popen(['diff', '-u', join(self.location, self.filename), join(self.location, self.filename + '.tmp')], stdout = PIPE).communicate()[0]
        output_to_file(output, self.name)

    def get_constructor(self, values):
        return {'file':SingleFileApplication(values)}

    def is_created(self):
        return lexists(join(self.location, self.filename))

    def __get_hidden_subfolder(self):
        return join(self.__get_hidden_dir(), self.directory)

    def __get_hidden_dir(self):
        return join (self.__get_hidden_root(), self.name)

    def __is_hidden_root_created(self):
        return lexists(self.__get_hidden_root())

    def __get_hidden_root(self):
        return join(self.location, '.file_repository')
