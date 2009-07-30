"""

Author: Kenneth Belizky
  
"""



class WSGIHandler(object):
    """
    This class represents 
    """

    def __init__(self, app_folders):
        """
        Constructor
        
        apps -- 
        """
        self._app_folders = app_folders

    def write_file(self, file_name, settings_path):
        """
        method able to write join and write the wsgi file
        """
        wsgi_file = open(file_name, 'w')
        wsgi_file.writelines([
            'import os\n',
            'import sys\n',
            'sys.stdout = sys.stderr\n',
            'from os.path import abspath, dirname, join\n',
            'from site import addsitedir\n',
            'path = addsitedir(abspath(join(dirname(__file__), \'django-hotclub\', \'external_libs\')), set())\n',
            'if path: sys.path = list(path) + sys.path\n'])

        #add all folders to python path
        for folder in self._app_folders:
            wsgi_file.write('sys.path.insert(0, abspath(\'%s\'))\n' % folder)

        wsgi_file.writelines([
            '\n',
            'from django.core.handlers.wsgi import WSGIHandler\n',
            '\n',
            'os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'%s\'\n' % settings_path,
            '\n',
            'application = WSGIHandler()\n' ])

if __name__ == '__main__':
    wsgi_handler = WSGIHandler(['a', 'b'])
    wsgi_handler.write_file('django.wsgi.tmp', 'lala')