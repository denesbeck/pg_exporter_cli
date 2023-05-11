import typer
from typing import Optional

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from app import backup, config, SUCCESS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR, SECTION_NOT_FOUND, CONFIG_NOT_FOUND, CONFIG_ALREADY_EXIST, DATABASE_ERROR, S3_ERROR, __app_name__, __version__

app = typer.Typer()
config_app = typer.Typer()
backup_app = typer.Typer()
migrate_app = typer.Typer()

configuration_not_found_default_message = "[red]Configuration doesn't exist[/red]"

app.add_typer(config_app, name="config")
app.add_typer(backup_app, name="backup")
app.add_typer(migrate_app, name="migrate")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def get_version(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@config_app.command("init")
def init() -> None:
    """Initialize configuration file and directory."""
    result = config.init()
    if result == SUCCESS:
        print("[green]Configuration initialized successfully[/green]")
    elif result == CONFIG_DIR_ERROR:
        print("[red]Configuration directory error[/red]")
    elif result == CONFIG_FILE_ERROR:
        print("[red]Configuration file error[/red]")
    elif result == CONFIG_ALREADY_EXIST:
        print("[red]Configuration already exists[/red]")


@config_app.command("destroy")
def destroy() -> None:
    """Destroy configuration file and directory."""
    result = config.destroy()
    if result == SUCCESS:
        print("[green]Configuration destroyed successfully[/green]")
    elif result == CONFIG_DIR_ERROR:
        print("[red]Unable to remove directory[/red]")
    elif result == CONFIG_FILE_ERROR:
        print("[red]Unable to remove config file[/red]")
    elif result == CONFIG_NOT_FOUND:
        print(configuration_not_found_default_message)


@config_app.command("register")
def register() -> None:
    """Register a database."""
    name = typer.prompt("Name")
    host = typer.prompt("Host")
    port = typer.prompt("Port")
    database = typer.prompt("Database")
    user = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True,
                            confirmation_prompt=True)
    result = config.register_database(
        name, host, port, database, user, password)
    if result == SUCCESS:
        print(
            f"[green]Database {name} registered successfully[/green]")
    elif result == CONFIG_WRITE_ERROR:
        print(f"[red]Unable to register database {name}[/red]")
    elif result == CONFIG_NOT_FOUND:
        print("[red]Configuration doesn't exist. Please initialize configuration.[/red]")


@config_app.command("unregister")
def unregister() -> None:
    """Unregister a database."""
    name = typer.prompt("Name")
    result = config.unregister_database(name)
    if result == SUCCESS:
        print(
            f"[green]Database {name} unregistered successfully[/green]")
    elif result == CONFIG_WRITE_ERROR:
        print(f"[red]Unable to unregister database {name}[/red]")
    elif result == SECTION_NOT_FOUND:
        print(f"[red]Database {name} not found[/red]")
    elif result == CONFIG_NOT_FOUND:
        print("[red]Configuration doesn't exist. Please initialize configuration.[/red]")


@config_app.command("list")
def list_databases():
    """List registered databases."""
    result = config.list_databases()
    if result == CONFIG_NOT_FOUND:
        print(configuration_not_found_default_message)
    elif len(result) == 0:
        return print("[red]No databases registered[/red]")
    else:
        print("[bold]Registered databases[/bold]")
        for database in result:
            print(f"[green]{database}[/green]")


@config_app.command("read")
def read_database_config():
    """Read database configuration."""
    name = typer.prompt("Name")
    result = config.read_database_config(name)
    if result == CONFIG_NOT_FOUND:
        print(configuration_not_found_default_message)
    elif result == SECTION_NOT_FOUND:
        print(f"[red]Database {name} not found[/red]")
    else:
        print("[bold]Database configuration[/bold]")
        table = Table("Key", "Value")
        table.add_row("Host", result["host"])
        table.add_row("Port", result["port"])
        table.add_row("Database", result["database"])
        table.add_row("User", result["user"])
        table.add_row("Password", result["password"])
        print(table)


@config_app.command("path")
def show_config_path():
    """Show configuration file path."""
    print(f"[cyan]{config.CONFIG_FILE_PATH}[/cyan]")


@backup_app.command("dump")
def dump_database():
    """Dump database and upload it to AWS S3."""
    name = typer.prompt("Name")
    result = backup.dump_database(name)
    if result == CONFIG_NOT_FOUND:
        print(configuration_not_found_default_message)
    elif result == DATABASE_ERROR:
        print(f"[red]Database {name} not found[/red]")
    elif result == SUCCESS:
        print(f"[green]Database {name} dumped successfully[/green]")
    elif result == S3_ERROR:
        print(f"[red]Unable to upload database {name} to S3[/red]")


@backup_app.command("list")
def list_backups():
    """List backups."""
    result = backup.list_backups()
    if result == S3_ERROR:
        print("[red]Unable to list backups[/red]")
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Listing...", total=None)
            table = Table("#", "Backup Name")
            for index, item in enumerate(result):
                table.add_row(str(index+1), item)
            print(table)


@backup_app.command("restore")
def restore_backup():
    """Restore backup."""
    backup_name = typer.prompt("Backup name")
    target_database = typer.prompt("Target database")
    result = backup.restore_backup(backup_name, target_database)
    if result == S3_ERROR:
        print(f"[red]Unable to restore backup {backup_name}[/red]")
    elif result == CONFIG_NOT_FOUND:
        print(configuration_not_found_default_message)
    elif result == DATABASE_ERROR:
        print(f"[red]Database {target_database} not found[/red]")
    elif result == SUCCESS:
        print(f"[green]Backup {backup_name} restored successfully[/green]")
