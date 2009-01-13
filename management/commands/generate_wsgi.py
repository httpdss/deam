#!/usr/bin/python

import os, sys, subprocess, logging
import optparse

from os.path import exists, join
from os import pathsep
from string import split
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deam.management.apps_manager import AppsManager

#taken from django_extensions
from deam.management.utils import get_project_root

class Command(BaseCommand):

    help = 'Generate a wsgi file for a project based on external apps'

    def handle(self, *args, **options):
        """
        wsgi generator command handler
        """
        self.apps_manager = AppsManager(get_project_root())
        self.apps_manager.generate_wsgi()

# vim: ai ts=4 sts=4 et sw=4
