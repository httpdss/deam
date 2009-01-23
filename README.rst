========================================
DEAM (Django External Apps Manager) 
========================================

**IMPORTANT: not for use on production sites (for now)**

This project is focused on resolving the recurring problem of managing external apps when working with django projects by taking a different approach: custom commands.

Installation and Settings
=========================

#. Download application from Github
#. Make sure the application is under a django project or is added to the python path
#. Edit your project's settings.py and add a DEAM_CONFIG dictionary if you dont like the defaults. You can override any default you want.
#. Execute 'python manage.py get_apps'

Format for the apps file::

    <apps>
        <app>
            <name></name>
            <url></url>
            <repo_type></repo_type>
            <directory></directory>
        </app>
        ...
        ...
    </apps>
    
Default DEAM_CONFIG::

    DEAM_CONFIG = {
        'apps_file': 'externalapps.xml',
        'prefix': '.',
        'suffix': 'repo',
        'alert' : True,
        'repos': { 
            'svn': 'svn',
            'hg': 'hg',
            'git': 'git',
            },  
        }

New in 0.6.2
============
- added alert support. If set to True, every time a repository is created for an application, deam will issue an alert, advising you to add the new app path to the python path.˝

New in 0.6.1
============
- custom exceptions, code cleanup

New in 0.6
==========
- config.xml and externalapps.xml support

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
