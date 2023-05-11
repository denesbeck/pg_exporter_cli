import gzip
import os
import time

from sh import pg_dump, pg_restore
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from app import s3, config, CONFIG_NOT_FOUND, DATABASE_ERROR, S3_ERROR, BACKUP_FILE_ERROR, SUCCESS


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
            return CONFIG_NOT_FOUND

        env = {'PGPASSWORD': db_config['password']}

        progress.add_task(description="Processing...", total=None)
        try:
            with gzip.open(backup_file_name, 'wb') as f:
                pg_dump('-h', db_config['host'], '-p',
                        db_config['port'], '-d', db_config['database'], '-U', db_config['user'], '-Fc', '-b', '-v',  _env=env, _out=f)
                progress.add_task(description="Uploading...", total=None)
                s3_res = s3.upload_file(backup_file_name)
                return s3_res
        except Exception:
            return DATABASE_ERROR
        finally:
            _delete_backup_file(backup_file_name)


def list_backups() -> int | list:
    return s3.list_backups()


def restore_backup(backup_name: str, target_database: str) -> int:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Preparing...", total=None)
        db_config = config.read_database_config(target_database)

        if db_config == CONFIG_NOT_FOUND:
            return CONFIG_NOT_FOUND

        env = {'PGPASSWORD': db_config['password']}

        s3_res = s3.restore_backup(backup_name)
        if s3_res == S3_ERROR:
            return S3_ERROR

        progress.add_task(description="Restoring...", total=None)
        try:
            with gzip.open(backup_name, 'rb') as f:
                pg_restore('-h', db_config['host'], '-p',
                           db_config['port'], '-d', db_config['database'], '-U', db_config['user'], '-v',  _env=env, _in=f)
            return SUCCESS
        except Exception as e:
            print(e)
            return DATABASE_ERROR
        finally:
            _delete_backup_file(backup_name)


def _delete_backup_file(backup_file_name: str):
    try:
        os.remove(backup_file_name)
    except OSError:
        return BACKUP_FILE_ERROR
