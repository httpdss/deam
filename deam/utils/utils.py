from django.conf import settings
from os.path import lexists
import os
import re
import fileinput


def get_patch_directory():
    if hasattr(settings, 'PATCH_DIR'):
        pre = settings.PATCH_DIR
    else:
        pre = '.patch'
    return os.path.join(get_project_root(), pre) 

def get_revision(revision):
    rev = -1
    m = re.search('Revision: (\d+)', revision)
    if m: 
        rev = m.group(1)
    return str(rev)

def get_project_root():
    """ get the project root directory """
    settings_mod = __import__(settings.SETTINGS_MODULE, {}, {}, [''])
    return os.path.dirname(os.path.abspath(settings_mod.__file__))

def output_file(name):
    try:
        fd = open(os.path.join(get_patch_directory(), name), 'r')
        lines = fd.readlines()
        for line in lines:
            print line,
    except IOError:
        pass
        
def output_to_file(output, name:
    final = output.splitlines()
    if final:
        if not(lexists(get_patch_directory())):
            os.makedirs(get_patch_directory())
        fd = open(os.path.join(get_patch_directory(), name), 'w')
        for line in final:
            fd.write(line + '\n')
        fd.close()

def directory_for_file(dir_name, file_name):
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            head,tail=os.path.split(dirfile)
            if tail == file_name:
                fileList.append(head)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile):
            fileList.extend(directory_for_file(dirfile,file_name))
    return fileList

def detect_type(url):
    """
    method that tries to infer which is the type of the respository
    
    url -- url of repository
    """
    if 'svn' in url:
        return 'svn'
    elif 'git' in url:
        return 'git'
    elif 'hg' in url:
        return 'hg'
    else:
        return None


class TermColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# vim: ai ts=4 sts=4 et sw=4
