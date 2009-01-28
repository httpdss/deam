#!/usr/bin/python

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from deam.utils.apps_manager import AppsManager

#taken from django_extensions
from deam.utils.utils import get_project_root

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-a',
            '--all',
            action='store_true',
            dest='get_all_apps',
            help='Download all external applications'),
        make_option(
            '-l',
            '--list-apps',
            action="store_true",
            dest='list_apps',
            help='List all external applications'),
        )

    help = 'Download all external apps defined for your django project'

    args="[external_appname ...]"

    def handle(self, app_name='', *args, **options):
        """
        external apps command handler
        """
        DEAM_CONFIG = {}
        if hasattr(settings, 'DEAM_CONFIG'):
            DEAM_CONFIG = settings.DEAM_CONFIG
        apps_manager = AppsManager(
            get_project_root(),
            DEAM_CONFIG,
        )

        get_all_apps = options.get('get_all_apps',False)
        list_apps = options.get('list_apps',False)

        if app_name:
            apps_manager.download_app(app_name)

        if get_all_apps:
            apps_manager.download_app()
        elif list_apps:
            apps_manager.list_external_apps()

# vim: ai ts=4 sts=4 et sw=4
