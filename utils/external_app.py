class ExternalApp(object):
    """
    This class represents representation of external application
    """

    def __init__(self, name, url, vcs_type='svn', directory=''):
        """
        Constructor.
        vcs_type -- type of the version control system. possible
                    values: svn, git and hg
        url -- url of repository
        folder -- project subfolder
        """
        self._vcs_type = vcs_type
        self._url = url
        self._name = name
        self._directory = directory

    def get_vcs_type(self):
        return self._vcs_type

    def set_vcs_type(self, vcs):
        self._vcs_type = vcs

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_directory(self):
        return self._directory

    def set_directory(self, directory):
        self._directory = directory

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def __unicode__(self):
        return "%s - %s" % (self._name, self._url)


    vcs_type = property(get_vcs_type, set_vcs_type)
    name = property(get_name, set_name)
    url = property(get_url, set_url)
    directory = property(get_directory, set_directory)

# vim: ai ts=4 sts=4 et sw=4
