from subprocess import call
from deam.utils.base_repository import BaseRepository


class SvnRepo(BaseRepository):

    def update(self):

        call(['svn','update'])

    def create(self):
        
        call(['svn','co', self.url, self.name])


class GitRepo(BaseRepository):

    def update(self):

        call(['git', 'pull'])

    def create(self):
        
        call(['git', 'clone', self.url, self.name])


class HgRepo(BaseRepository):
    
    def update(self):

        call(['hg', 'pull', '-u'])

    def create(self):
        print 'entro?'
        call(['hg', 'clone', self.url, self.name])