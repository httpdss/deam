#!/usr/bin/python

import os, sys, subprocess, logging
import pysvn
import optparse

from os.path import exists, join
from os import pathsep
from string import split
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from external_downloads.management.apps_manager import AppsManager

#taken from django_extensions
from external_downloads.management.utils import get_project_root

class Command(BaseCommand):

    help = 'Download all external apps defined for your django project'

    def handle(self, *args, **options):
        """
        external apps command handler
        """
        self.apps_manager = AppsManager(get_project_root())
        self.apps_manager.execute()

# vim: ai ts=4 sts=4 et sw=4
