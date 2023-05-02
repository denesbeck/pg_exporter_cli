import gzip
import os
import time

from sh import pg_dump
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from app import s3, config, CONFIG_NOT_FOUND, DATABASE_NOT_FOUND


def dump_database(name: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Preparing...", total=None)
        db_config = config.read_database_config(name)

        global backup_file_name

        backup_file_name = f"{db_config['database']}_{time.strftime('%Y-%m-%d_%H:%M:%S')}.dump.gz"

        if db_config == CONFIG_NOT_FOUND:
            return print("[red]Configuration doesn't exist[/red]")

        env = {'PGPASSWORD': db_config['password']}

        progress.add_task(description="Processing...", total=None)
        try:
            with gzip.open(backup_file_name, 'wb') as f:
                pg_dump('-h', db_config['host'], '-p',
                        db_config['port'], '-U', db_config['user'], '-Fc', '-b', '-v', '-d', db_config['database'], _env=env, _out=f)
        except Exception:
            return DATABASE_NOT_FOUND

        progress.add_task(description="Uploading...", total=None)
        s3_res = s3.upload_file(backup_file_name)

        _delete_backup_file()

        return s3_res


def list_backups() -> int | list:
    return s3.list_backups()


def restore_backup(name: str) -> int:
    s3.restore_backup(name)


def _delete_backup_file():
    try:
        os.remove(backup_file_name)
    except OSError:
        pass
