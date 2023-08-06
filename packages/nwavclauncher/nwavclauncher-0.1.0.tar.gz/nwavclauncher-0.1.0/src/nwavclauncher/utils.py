
"""-"""
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("nw." + __name__)  # pylint: disable=invalid-name


class ConfigError(Exception):
    """-"""


@dataclass
class ConfigData:
    avcoder_id: str
    access_key: str
    root_domain: str

    @property
    def avcbroker_url(self) -> str:
        """-"""
        if os.environ.get("NW_AVCBROKER_ENDPOINT"):
            return os.environ["NW_AVCBROKER_ENDPOINT"]
        else:
            return "https://content-avcbroker.api.{}".format(
                self.root_domain)


def get_app_dir() -> str:
    """COPIED FROM NWAVCODER DON'T CHANGE!"""

    nw_folder_name: str = "nativewaves"
    avc_folder_name: str = "avcoder"

    if os.name == "nt":
        local_app_dir: Optional[str] = os.getenv("LOCALAPPDATA")
        if not local_app_dir:
            raise IOError("Cannot load local app directory")
        app_dir = os.path.join(
            local_app_dir,
            nw_folder_name,
            avc_folder_name)

    elif os.name == "posix":
        app_dir = os.path.join(
            Path.home().resolve(),
            nw_folder_name,
            avc_folder_name)

    else:
        raise NotImplementedError()

    app_dir = app_dir.replace(os.sep, "/")
    return app_dir


def get_config_path() -> str:
    """COPIED FROM NWAVCODER DON'T CHANGE!"""
    return get_app_dir() + "/config.json"


def load_config() -> ConfigData:
    """-"""

    try:
        config_path: str = get_config_path()
        with open(config_path) as file:
            data: Dict[str, Any] = dict(json.loads(file.read()))
            return ConfigData(
                str(data["avcoderId"]),
                str(data["accessKey"]),
                str(data.get("rootDomain", "nativewaves.com"))
            )
    except Exception as ex:  # pylint: disable=broad-except
        raise ConfigError("Could not load config data. {} {}".format(
            type(ex).__name__, ex))


def login(config: ConfigData) -> str:
    """Perfoms login and returns bearer access token"""

    response = requests.post(
        "{}/auth/login".format(config.avcbroker_url,),
        auth=HTTPBasicAuth(config.avcoder_id, config.access_key))
    response.raise_for_status()
    data = json.loads(response.content)
    return str(data["accessToken"])


# def download_nwavcoder(access_token: str, version: str = "latest") -> None:
#     """-"""

#     response = requests.get(
#         "{}/software/{}/versions/{}/download".format(
#             config.avcbroker_url,
#             "main",
#             version
#         ),
#         auth=HTTPBasicAuth(config.avcoder_id, config.access_key),
#         allow_redirects=True)

