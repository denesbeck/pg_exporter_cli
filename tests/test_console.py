from typer.testing import CliRunner
from cli import console, config, __app_name__, __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(console.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init_1():
    result = runner.invoke(console.app, ["config", "init"])
    assert result.exit_code == 0
    assert 'Configuration initialized successfully\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is True


def test_init_2():
    result = runner.invoke(console.app, ["config", "init"])
    assert result.exit_code == 0
    assert 'Configuration already exists\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is True


def test_destroy():
    result = runner.invoke(console.app, ["config", "destroy"])
    assert result.exit_code == 0
    assert 'Configuration destroyed successfully\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is False
