import os
import configparser
import typer

from pathlib import Path
from app import __app_name__, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR, CONFIG_WRITE_ERROR, SECTION_NOT_FOUND, CONFIG_NOT_FOUND, CONFIG_ALREADY_EXIST, SUCCESS

from dotenv import load_dotenv
load_dotenv()

app_env = os.environ.get("APP_ENV")

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))

if app_env != 'production':
    CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__)) / app_env

CONFIG_FILE_PATH = CONFIG_DIR_PATH / 'config.ini'


def init() -> int:
    if _check_if_exists() is True:
        return CONFIG_ALREADY_EXIST

    try:
        print(CONFIG_DIR_PATH)
        CONFIG_DIR_PATH.mkdir(exist_ok=True, parents=True)
    except OSError:
        return CONFIG_DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return CONFIG_FILE_ERROR
    return SUCCESS


def register_database(name: str, host: str, port: str, database: str, user: str, password: str) -> int:
    if _check_if_exists() is False:
        return CONFIG_NOT_FOUND

    config_parser = configparser.ConfigParser()
    config_parser[name] = {"host": host, "port": port, "database": database,
                           "user": user, "password": password}
    try:
        with open(CONFIG_FILE_PATH, 'a') as config_file:
            config_parser.write(config_file)
    except OSError:
        return CONFIG_WRITE_ERROR
    return SUCCESS


def unregister_database(name: str) -> int:
    if _check_if_exists() is False:
        return CONFIG_NOT_FOUND

    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_FILE_PATH)
    result = config_parser.remove_section(name)

    if result is False:
        return SECTION_NOT_FOUND

    try:
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            config_parser.write(config_file)
    except OSError:
        return CONFIG_WRITE_ERROR
    return SUCCESS


def list_databases() -> list:
    if _check_if_exists() is False:
        return CONFIG_NOT_FOUND

    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_FILE_PATH)
    return config_parser.sections()


def read_database_config(name: str) -> dict | int:
    if _check_if_exists() is False:
        return CONFIG_NOT_FOUND

    config_parser = configparser.ConfigParser()
    try:
        config_parser.read(CONFIG_FILE_PATH)
        return config_parser[name]
    except KeyError:
        return SECTION_NOT_FOUND


def destroy() -> int:
    if _check_if_exists() is False:
        return CONFIG_NOT_FOUND

    try:
        CONFIG_FILE_PATH.unlink()
    except OSError:
        return CONFIG_FILE_ERROR
    try:
        CONFIG_DIR_PATH.rmdir()
    except OSError:
        return CONFIG_DIR_ERROR
    return SUCCESS


def _check_if_exists() -> bool:
    return CONFIG_FILE_PATH.exists()
