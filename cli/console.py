import typer

from rich import print

from cli import config, messages, SUCCESS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR

app = typer.Typer()
config_app = typer.Typer()
dumper_app = typer.Typer()

app.add_typer(config_app, name="config")
app.add_typer(dumper_app, name="dump")


@config_app.command("init")
def init():
    """Initialize configuration file and directory."""
    result = config.init()
    if result == SUCCESS:
        print("[green]Configuration initialized successfully[/green]")
    elif result == CONFIG_DIR_ERROR:
        print(f"[red]{messages[CONFIG_DIR_ERROR]}[/red]")
    elif result == CONFIG_FILE_ERROR:
        print(f"[red]{messages[CONFIG_FILE_ERROR]}[/red]")


@config_app.command("destroy")
def destroy():
    """Destroy configuration file and directory."""
    result = config.destroy()
    if result == SUCCESS:
        print("[green]Configuration destroyed successfully[/green]")
    elif result == CONFIG_DIR_ERROR:
        print("[red]Unable to remove directory[/red]")
    elif result == CONFIG_FILE_ERROR:
        print("[red]Unable to remove config file[/red]")


@config_app.command("register")
def register():
    name = typer.prompt("Name")
    host = typer.prompt("Host")
    port = typer.prompt("Port")
    user = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True,
                            confirmation_prompt=True)
    result = config.register_database(name, host, port, user, password)
    if result == SUCCESS:
        print(f"[green]Database {name} registered successfully[/green]")
    elif result == CONFIG_WRITE_ERROR:
        print(f"[red]Unable to register database {name}[/red]")
