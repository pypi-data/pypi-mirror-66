from __future__ import print_function

from trakt_tools.core.authentication import authenticate
from trakt_tools.tasks import CreateBackupTask

import click
import os


@click.command('profile:backup:create')
@click.option(
    '--token',
    default=None,
    help='Trakt.tv authentication token. (default: prompt)'
)
@click.option(
    '--backup-dir',
    default=None,
    help='Directory that backups should be stored in. (default: "./backups")'
)
@click.option(
    '--per-page',
    default=1000,
    help='Request page size. (default: 1000)'
)
@click.pass_context
def profile_backup_create(ctx, token, backup_dir, per_page):
    """Create backup of a Trakt.tv profile."""

    if not token:
        success, token = authenticate()

        if not success:
            print('Authentication failed')
            exit(1)

        print()

    # Set default backup directory
    if not backup_dir:
        backup_dir = os.path.join(os.curdir, 'backups')

    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Run task
    success = CreateBackupTask(
        backup_dir=backup_dir,
        per_page=per_page,

        debug=ctx.parent.debug,
        rate_limit=ctx.parent.rate_limit
    ).run(
        token=token
    )

    if not success:
        exit(1)
