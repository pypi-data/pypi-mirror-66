from requests.exceptions import HTTPError

from mgsc.service import Gitea


class GiteaMigration:
    def __init__(
        self,
        giteaurl,
        giteauser,
        giteapassword,
        giteagroupname,
        reponame,
        repodescription,
        sourcecloneurl,
        sourceuser,
        sourcesecret,
    ):
        self.gitea = Gitea(url=giteaurl, username=giteauser, secret=giteapassword)
        self.giteagroupname = giteagroupname
        self.reponame = reponame
        self.repodescription = repodescription
        self.sourcecloneurl = sourcecloneurl
        self.sourceuser = sourceuser
        self.sourcesecret = sourcesecret

    def _get_gitea_group_id(self):
        urlpath = f"{Gitea.API_BASE}/orgs/{self.giteagroupname}"
        return self.gitea.session.httpaction(http_verb="get", path=urlpath).json()["id"]

    def _get_migration_payload(self,):
        return {
            "auth_password": self.sourcesecret,
            "auth_username": self.sourceuser,
            "clone_addr": self.sourcecloneurl,
            "description": self.repodescription,
            "issues": True,
            "labels": True,
            "milestones": True,
            "mirror": True,
            "private": True,
            "pull_requests": True,
            "releases": True,
            "repo_name": self.reponame,
            "uid": self._get_gitea_group_id(),
            "wiki": True,
        }

    def create_migration(self):
        urlpath = f"{Gitea.API_BASE}/repos/migrate"
        response = self.gitea.session.httpaction(
            http_verb="post",
            path=urlpath,
            data=self._get_migration_payload(),
            xstatus=201,
        )
        return response

    def sync(self):
        urlpath = (
            f"{Gitea.API_BASE}/repos/{self.giteagroupname}/{self.reponame}/mirror-sync"
        )
        response = self.gitea.session.httpaction(http_verb="post", path=urlpath)
        return response

    def create_or_sync(self):
        try:
            self.create_migration()
        except HTTPError:
            self.sync()
