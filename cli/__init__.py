__app_name__ = 'pg_exporter_cli'
__version__ = "0.1.0"

(SUCCESS, CONFIG_DIR_ERROR, CONFIG_FILE_ERROR,
 CONFIG_WRITE_ERROR, SECTION_NOT_FOUND, CONFIG_NOT_FOUND) = range(6)

messages = {
    SUCCESS: "Success",
    CONFIG_DIR_ERROR: "Configuration directory error",
    CONFIG_FILE_ERROR: "Configuration file error",
    CONFIG_WRITE_ERROR: "Configuration write error",
    SECTION_NOT_FOUND: "Section not found",
}
