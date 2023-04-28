import typer
from typing import Optional

from rich import print

from cli import config, SUCCESS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR, SECTION_NOT_FOUND, CONFIG_NOT_FOUND, CONFIG_ALREADY_EXIST, __app_name__, __version__

app = typer.Typer()
config_app = typer.Typer()
dumper_app = typer.Typer()

app.add_typer(config_app, name="config")
app.add_typer(dumper_app, name="dump")


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
        print("[red]Configuration doesn't exist[/red]")


@config_app.command("register")
def register() -> None:
    """Register a database."""
    name = typer.prompt("Name")
    host = typer.prompt("Host")
    port = typer.prompt("Port")
    user = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True,
                            confirmation_prompt=True)
    result = config.register_database(name, host, port, user, password)
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
        print("[red]Configuration doesn't exist[/red]")
    elif len(result) == 0:
        return print("[red]No databases registered[/red]")
    else:
        print("[bold]Registered databases[/bold]")
        for database in result:
            print(f"[green]{database}[/green]")


@config_app.command("path")
def show_config_path():
    """Show configuration file path."""
    print(f"[cyan][bold]{config.CONFIG_FILE_PATH}[/bold][/cyan]")
