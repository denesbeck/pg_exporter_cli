from typer.testing import CliRunner
from cli import console, config, __app_name__, __version__

runner = CliRunner()
app = console.app


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init_1():
    result = runner.invoke(app, ["config", "init"])
    assert result.exit_code == 0
    assert 'Configuration initialized successfully\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is True


def test_init_2():
    result = runner.invoke(app, ["config", "init"])
    assert result.exit_code == 0
    assert 'Configuration already exists\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is True


def test_list_empty():
    result = runner.invoke(app, ["config", "list"])
    assert result.exit_code == 0
    assert 'No databases registered\n' in result.stdout


def test_register():
    result = runner.invoke(app, [
                           "config", "register"], input='test-1\nhost-1\n5432\nuser-1\npwd-1\npwd-1\n')
    assert result.exit_code == 0
    assert 'Database test-1 registered successfully\n' in result.stdout

    result = runner.invoke(app, [
                           "config", "register"], input='test-2\nhost-2\n5432\nuser-2\npwd-2\npwd-2\n', )
    assert result.exit_code == 0
    assert 'Database test-2 registered successfully\n' in result.stdout

    result = runner.invoke(app, [
                           "config", "register"], input='test-3\nhost-3\n5432\nuser-3\npwd-3\npwd-3\n', )
    assert result.exit_code == 0
    assert 'Database test-3 registered successfully\n' in result.stdout

#     result = runner.invoke(app, [
#                            "config", "list"])
#     assert result.exit_code == 0
#     assert 'No databases registered\n' in result.stdout


def test_destroy():
    result = runner.invoke(app, ["config", "destroy"])
    assert result.exit_code == 0
    assert 'Configuration destroyed successfully\n' in result.stdout
    assert config.CONFIG_DIR_PATH.exists() is False
