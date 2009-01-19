========================================
DEAM (Django External Apps Manager) 
========================================

**IMPORTANT: not for use on production sites (for now)**

This project is focused on resolving the recurring problem of managing external apps when working with django projects by taking a different approach: custom commands.

Installation and Settings
=========================

#. Download application from Github
#. Make sure the application is under a django project or is added to the python path
#. create a file inside the external apps folders you want to use and name it 'external.apps' this is the file where to set the different sources. The current format is *<application_name> <repository url> <repository type> <source/destination directory>*
#. execute 'python manage.py get_apps'


New in 0.5
==========
- sub directory support

New in 0.4
==========
- mercurial support
- git support
- generalized download/update functions
- internal testing

New in 0.3
==========
- name change

New in 0.2
==========
- wsgi generator (under development)

New in 0.1
==========
- svn checkout
- folder scanning for the external.apps file
