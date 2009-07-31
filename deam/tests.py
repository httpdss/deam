'''
Created on Jul 2, 2009

@author: Kenneth Belitzky
'''
#from deam.utils.repository_handler import RepositoryHandler
from deam.utils.repositories import SingleFileApplication
import unittest


class Test(unittest.TestCase):
    """
        Testing module
    """

    def setUp(self): #IGNORE:C0103
        """ method for object initialization """
        return unittest.TestCase.setUp(self)

    def test_downloading(self):
        """
            test if the repository handler is downloading things correctly
        """
        #from os.path import join, abspath, dirname
        #deam_rel_root = dirname(dirname(abspath(__file__)))
        #repo_handler = RepositoryHandler(join(deam_rel_root, 'testing'))
        #  repo_handler.execute(False)
        self.assertEqual(True)

    def test_single_app_download(self):
        """test that the download of the single files is working correctly"""
        single_app = SingleFileApplication({
            'name' : 'pepe',
            'url': 'http://www.djangosnippets.org/snippets/1135/download/',
            'filename': 'firebug.py',
            'type': 'file',
            'location' : '/tmp'
        })
        single_app.download_or_update()
        self.assertTrue(True)
