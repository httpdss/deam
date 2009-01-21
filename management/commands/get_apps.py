#!/usr/bin/python

import os
import sys
import subprocess
import logging
import optparse

from os.path import exists, join
from os import pathsep
from string import split
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deam.utils.apps_manager import AppsManager

#taken from django_extensions
from deam.utils.utils import get_project_root

class Command(BaseCommand):

    help = 'Download all external apps defined for your django project'

    def handle(self, *args, **options):
        """
        external apps command handler
        """
        DEAM_CONFIG = {}
        if hasattr(settings, 'DEAM_CONFIG'):
            DEAM_CONFIG = settings.DEAM_CONFIG
        self.apps_manager = AppsManager(get_project_root(), DEAM_CONFIG)
        self.apps_manager.execute()

# vim: ai ts=4 sts=4 et sw=4
