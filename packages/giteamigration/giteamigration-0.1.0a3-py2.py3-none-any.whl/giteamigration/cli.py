"""Console script for gitback."""
import sys
import click

from requests.exceptions import HTTPError
from mgsc.service import Gitea, Github, Gitlab
from giteamigration.giteamigration import GiteaMigration


services = {"gitea": Gitea, "github": Github, "gitlab": Gitlab}


@click.command()
@click.option("--giteaurl", required=True, help="Gitea URL")
@click.option("--giteauser", required=True, help="Gitea user")
@click.option("--giteapass", required=True, help="Gitea password")
@click.option("--giteaorg", required=True, help="Gitea Organisation name")
@click.option("--sourcetype", required=True, help="Source GIT server type")
@click.option("--sourceurl", required=True, help="Source GIT server URL")
@click.option("--sourceuser", default=None, help="Source GIT server username")
@click.option("--sourcepass", default=None, help="Source GIT server password")
@click.option(
    "--sourcerepos", default="*", help="Glob style pattern for repos to migrate"
)
def main(
    giteaurl,
    giteauser,
    giteapass,
    giteaorg,
    sourcetype,
    sourceurl,
    sourceuser,
    sourcepass,
    sourcerepos,
):
    RETURN_CODE_SUCCESS = 0
    RETURN_CODE_FAILED_PROCESS = 1
    RETURN_CODE_FAILED_MIGRATIONS = 2
    status = {
        "success": 0,
        "failed": 0,
    }
    print(f"sourcerepos: {sourcerepos}")
    sourceserver = get_source_gitserver(sourcetype, sourceurl, sourceuser, sourcepass)
    for repo in sourceserver.repositories_filtered(sourcerepos):
        print("------------------------")
        print(f"Migrating repo: {repo}")
        migration = get_gitea_migration(
            giteaurl,
            giteauser,
            giteapass,
            giteaorg,
            repo.name,
            repo.description,
            repo.http_url,
            sourceuser,
            sourcepass,
        )
        try:
            migration.create_migration()
            print(f"Migration created succesfully: {repo}")
            status["success"] += 1
            print("------------------------\n")
            continue
        except HTTPError as e:
            if e.args[0]["code"] == 409:
                print(f"Migration already exists: {repo}. Synchronising migration.")
            else:
                print(e)
                status["failed"] += 1
                print("------------------------\n")

        try:
            migration.sync()
            print(f"Migration synchronised succesfully: {repo}")
            print("------------------------\n")
            status["success"] += 1
        except HTTPError as e:
            print(e)
            print(f"Synchronisation failed: {repo}")
            print("------------------------\n")
            status["failed"] += 1

    print("")
    print("==================")
    print("Migration complete.")
    print(f'Successfully migrations: {status["success"]}')
    print(f'Failed migrations: {status["success"]}')
    if status["failed"] > 0:
        return RETURN_CODE_FAILED_MIGRATIONS
    if status["failed"] == 0 and status["success"] > 0:
        return RETURN_CODE_SUCCESS
    return RETURN_CODE_FAILED_PROCESS


def get_source_gitserver(servertype, url, user, password):
    return services[servertype](url=url, username=user, secret=password)


def get_gitea_migration(
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
    return GiteaMigration(
        giteaurl,
        giteauser,
        giteapassword,
        giteagroupname,
        reponame,
        repodescription,
        sourcecloneurl,
        sourceuser,
        sourcesecret,
    )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
