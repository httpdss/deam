'''
get_apps.py - 
'''

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from deam.utils.apps_manager import AppsManager
from deam.utils.utils import get_project_root

class Command(BaseCommand):
    '''
    Implementation of the command class
    '''
    
    option_list = BaseCommand.option_list + (
        make_option(
            '-a',
            '--all',
            action = 'store_true',
            dest = 'get_all_apps',
            help = 'Download all external applications'),
        make_option(
            '-s',
            '--show-details',
            action = "store_true",
            dest = 'show_details',
            help = 'Show details for the specified application'),
        make_option(
            '-l',
            '--list-apps',
            action = "store_true",
            dest = 'list_apps',
            help = 'List all external applications'),
        )

    help = 'Download all external apps defined for your django project'

    args = "[external_appname]"

    def handle(self, app_name = '', *args, **options):
        """
        external apps command handler
        """
        deam_config = {}
        if hasattr(settings, 'DEAM_CONFIG'):
            deam_config = settings.DEAM_CONFIG
        apps_manager = AppsManager(
            get_project_root(),
            deam_config,
        )

        get_all_apps = options.get('get_all_apps', False)
        list_apps = options.get('list_apps', False)

        if app_name:
            apps_manager.download_app(app_name)

        if get_all_apps:
            apps_manager.download_app()
        elif list_apps:
            apps_manager.list_external_apps()
        elif not app_name:
            print "Missing params"
