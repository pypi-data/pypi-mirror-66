import os
import logging
from sqlalchemy import engine_from_config
from configparser import ConfigParser
import re

logger = logging.getLogger(__name__)


def credd_from_odbc_ini():
    credential_filename = os.getenv(
        "NUVOLOS_CREDENTIAL_FILENAME", os.path.expanduser("~") + "/.odbc.ini"
    )
    credential_section = os.getenv("NUVOLOS_CREDENTIAL_SECTION", "nuvolos")
    # Create engine with credentials
    cred = ConfigParser(interpolation=None)
    if not os.path.exists(credential_filename):
        raise FileNotFoundError(f"Credentials file {credential_filename} not found")
    cred.read(credential_filename)
    if not cred.has_section(credential_section):
        raise ValueError(
            f"Could not find section '{credential_section}' in odbc.ini file {credential_filename}. "
            f"Please add your Nuvolos Snowflake credentials there "
            f"(your username as 'uid' and your Snowflake access token as 'pwd')."
        )
    odbc_ini = dict(cred.items(credential_section))
    if "uid" not in odbc_ini:
        raise ValueError(
            f"Could not find option 'uid' in the '{credential_section}' "
            f"section of odbc.ini file {credential_filename}. "
            f"Please set it to your Nuvolos username"
        )
    if "pwd" not in odbc_ini:
        raise ValueError(
            f"Could not find option 'pwd' in the '{credential_section}' "
            f"section of odbc.ini file {credential_filename}. "
            f"Please set it to your Nuvolos Snowflake access token"
        )
    return {"username": odbc_ini["uid"], "snowflake_access_token": odbc_ini["pwd"]}


def get_dbpath():
    path_filename = os.getenv("NUVOLOS_DBPATH_FILE", "/lifecycle/.dbpath")
    if not os.path.exists(path_filename):
        logger.debug(
            f"Could not find dbpath file {path_filename}, looking at ~/.dbpath instead"
        )
        path_filename = os.path.expanduser("~") + "/.dbpath"
        if not os.path.exists(path_filename):
            logger.debug(f"Could not find dbpath file {path_filename}")
            return None, None
    with open(path_filename, "r") as path_file:
        lines = path_file.readlines()
        if len(lines) == 0:
            logger.debug(f"Could not parse dbpath file: {path_filename} is empty.")
            return None, None
        first_line = lines[0].rstrip()
        if "Tables are not enabled" in first_line:
            raise Exception(
                f"Tables are not enabled for this space, please enable them first"
            )
        # Split at "." character
        # This should have resulted in two substrings
        split_arr = re.split('"."', first_line)
        if len(split_arr) != 2:
            logger.debug(
                f'Could not parse dbpath file: pattern "." not found in {path_filename}. '
                f"Are the names escaped with double quotes?"
            )
            return None, None
        # Split removes the two quotes
        db_name = split_arr[0] + '"'
        schema_name = '"' + split_arr[1]
        logger.debug(
            f"Found database = {db_name}, schema = {schema_name} in dbpath file {path_filename}."
        )

        return db_name, schema_name


def get_url(username=None, password=None, dbname=None, schemaname=None):
    credd = {"username": username, "snowflake_access_token": password}
    if username is None and password is None:
        username_filename = os.getenv("NUVOLOS_USERNAME_FILENAME", "/secrets/username")
        snowflake_access_token_filename = os.getenv(
            "NUVOLOS_SNOWFLAKE_ACCESSS_TOKEN_FILENAME",
            "/secrets/snowflake_access_token",
        )
        if not os.path.exists(username_filename) or not os.path.exists(
            snowflake_access_token_filename
        ):
            logger.debug(
                f"Could not find file(s) /secrets/username or /secrets/snowflake_access_token, "
                f"looking for ~/.odbc.ini instead"
            )
            credd = credd_from_odbc_ini()
        else:
            with open(username_filename) as username, open(
                snowflake_access_token_filename
            ) as access_token:
                credd["username"] = username.readline()
                credd["snowflake_access_token"] = access_token.readline()
    elif username is not None and password is None:
        raise ValueError(
            "You have provided a username but not a password. "
            "Please either provide both arguments or leave both arguments empty."
        )
    elif username is None and password is not None:
        raise ValueError(
            "You have provided a password but not a username. "
            "Please either provide both arguments or leave both arguments empty."
        )

    if dbname is None and schemaname is None:
        db_name, schema_name = get_dbpath()
    elif dbname is not None and schemaname is None:
        raise ValueError(
            "You have provided a dbname argument but not a schemaname argument. "
            "Please either provide both or provide none of them."
        )
    elif dbname is None and schemaname is not None:
        raise ValueError(
            "You have provided a schemaname argument but not a dbname argument. "
            "Please either provide both or provide none of them."
        )
    else:
        db_name = dbname
        schema_name = schemaname

    default_snowflake_host = (
        "acstg.eu-central-1"
        if db_name is not None and "STAGING/" in db_name
        else "alphacruncher.eu-central-1"
    )
    snowflake_host = os.getenv("NUVOLOS_SNOWFLAKE_HOST", default_snowflake_host)
    url = (
        "snowflake://"
        + credd["username"]
        + ":"
        + credd["snowflake_access_token"]
        + "@"
        + snowflake_host
        + "/?warehouse="
        + credd["username"]
    )
    masked_url = (
        "snowflake://"
        + credd["username"]
        + ":"
        + "********"
        + "@"
        + snowflake_host
        + "/?warehouse="
        + credd["username"]
    )

    if db_name:
        url = url + "&database=" + db_name
        masked_url = masked_url + "&database=" + db_name
        if schema_name:
            url = url + "&schema=" + schema_name
            masked_url = masked_url + "&schema=" + schema_name
    logger.debug("Built SQLAlchemy URL: " + masked_url)
    return url


def get_engine(username=None, password=None, dbname=None, schemaname=None):
    return engine_from_config(
        {
            "sqlalchemy.url": get_url(username, password, dbname, schemaname),
            "sqlalchemy.echo": False,
        }
    )


def get_connection(username=None, password=None, dbname=None, schemaname=None):
    loc_eng = get_engine(username, password, dbname, schemaname)
    return loc_eng.connect()
