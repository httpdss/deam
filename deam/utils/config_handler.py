"""
    Config Handler
"""
import ConfigParser
from os.path import join

EXTERNAL_APPS_FILE = 'external.apps'

class ConfigHandler(object):
    """
    This class represents 
    """

    def __init__(self, location):
        """
        Constructor.
        """
        self.location = location

    def parse_apps_file(self):
        """parse an apps file """
        result = []
        config = ConfigParser.SafeConfigParser()
        config.read(join(self.location, EXTERNAL_APPS_FILE))
        for sec in config.sections():
            #get all items and assign name from the section name.
            temp = dict(config.items(sec) + 
                        [('name', sec), ('location', self.location)])
            result.append(temp)
        return result
