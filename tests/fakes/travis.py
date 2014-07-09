from app import app
from faker import Faker
import json
from random import Random

gen = Random()
fake = Faker()


class FakeTravisPayload:
    def __init__(self,
                 **kwargs):
        self.author_name = fake.name()
        self.author_email = fake.email()
        if gen.random() < 0.8:
            self.committer_name = self.author_name
            self.committer_email = self.author_email
        else:
            self.committer_name = fake.name()
            self.committer_email = fake.email()
        (repo_owner, repo_name) = app.config['GITHUB_REPO'].split('/')
        self.repo_owner =\
            kwargs['repo_owner'] if 'repo_owner' in kwargs else repo_owner
        self.repo_name =\
            kwargs['repo_name'] if 'repo_name' in kwargs else repo_name
        self.repo_url =\
            app.config['GITHUB_INSTALL']+self.repo_owner+'/'+self.repo_name
        self.args = {
            'id': 1,
            'number': "1",
            'status': None,
            'started_at': None,
            'finished_at': None,
            'status_message': "Passed",
            'commit': "62aae5f70ceee39123ef",
            'branch': "master",
            'message': "the commit message",
            'committed_at': "2011-11-11T11:11:11Z",
            'committer_name': self.committer_name,
            'committer_email': self.committer_email,
            'author_name': self.author_name,
            'author_email': self.author_email,
        }
        for x in self.args:
            if x in kwargs:
                self.args[x] = kwargs[x]

        self.args['repository'] = {
            "id": 1,
            "name": self.repo_name,
            "owner_name": self.repo_owner,
            "url": self.repo_url
        }

        self.args['config'] = {'notifications': {
                               'webhooks': ("http://example.net/notifications",
                                            "http://example.com/")
                               }}
        if 'webhooks' in kwargs:
            self.args['config']['notifications']['webhooks'] =\
                kwargs['webhooks']

        axis = {
            "id": 2,
            "repository_id": 1,
            "number": "1.1",
            "state": "created",
            "log": "",
            "parent_id": self.args['id'],
            "compare_url": self.repo_url + "/compare/master...develop"
            }
        for arg in 'commit',\
            'message',\
            'config',\
            'committed_at',\
            'started_at',\
            'finished_at',\
            'committer_name',\
            'committer_email',\
            'author_name',\
            'author_email',\
            'branch',\
            'status',\
            'result':
                if arg in self.args:
                    axis[arg] = self.args[arg]
        self.args['matrix'] = [axis]

    def __repr__(self):
        return json.dumps(self.args)
