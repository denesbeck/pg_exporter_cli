import typer

from rich import print

from cli import config, SUCCESS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR, SECTION_NOT_FOUND, CONFIG_NOT_FOUND

app = typer.Typer()
config_app = typer.Typer()
dumper_app = typer.Typer()

app.add_typer(config_app, name="config")
app.add_typer(dumper_app, name="dump")


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
    databases = config.list_databases()
    if not databases:
        print("[red]No databases registered[/red]")
    else:
        print("[bold]Registered databases[/bold]")
        for database in databases:
            print(f"[green]{database}[/green]")


@config_app.command("path")
def show_config_path():
    """Show configuration file path."""
    print(f"[cyan][bold]{config.CONFIG_FILE_PATH}[/bold][/cyan]")
