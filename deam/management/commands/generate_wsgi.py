"""
generate_wsgi.py - 
"""


from django.core.management.base import BaseCommand
from deam.utils.apps_manager import AppsManager

#taken from django_extensions
from deam.utils.utils import get_project_root

class Command(BaseCommand):
    """
    Command class that implements the generation of wsgi file.
    """

    help = 'Generate a wsgi file for a project based on external apps'

    def __init__(self):
        """
        Constructor for the wsgi generator
        """
        BaseCommand.__init__(self)
        self.apps_manager = AppsManager(get_project_root())

    def handle(self, *args, **options):  #IGNORE:W0613
        """
        wsgi generator command handler
        """
        self.apps_manager.generate_wsgi()
