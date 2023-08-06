# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Proxy utils module
"""
import os

from urllib.parse import urlparse, quote
from requests.utils import get_environ_proxies

from gmsaas.saas.api import CLOUD_BASE_URL
from gmsaas.storage import configcache as cfg
from gmsaas.gmsaas.logger import LOGGER


GMSAAS_PROXY_USERNAME_ENV = "GMSAAS_PROXY_USERNAME"
GMSAAS_PROXY_PASSWORD_ENV = "GMSAAS_PROXY_PASSWORD"


def get_proxy_info():
    """
    Return proxy "host:port" used or "" if there is none
    Proxy info is taken from config or from system
    We compare it with adbtunneld's one
    No authentication info is returned
    """
    url = cfg.get_proxy_url()

    if not url:
        proxies = get_environ_proxies(CLOUD_BASE_URL)
        url = proxies.get("https")

    if not url:
        return ""

    parsed_url = urlparse(url)
    return "{}:{}".format(parsed_url.hostname, parsed_url.port)


def get_proxies_from_config():
    """
    Return proxies dict usable by requests or None if no proxy is set
    """
    config_url = cfg.get_proxy_url()
    if not config_url:
        return None

    parsed_url = urlparse(config_url)

    username = parsed_url.username
    password = parsed_url.password

    username_env = quote(os.environ.get(GMSAAS_PROXY_USERNAME_ENV, ""), safe="")
    password_env = quote(os.environ.get(GMSAAS_PROXY_PASSWORD_ENV, ""), safe="")

    if username_env:
        username = username_env
    if password_env:
        password = password_env

    url = parsed_url.scheme + "://"
    if username:
        url += username
        if password:
            url += ":" + password
        url += "@"
    url += parsed_url.hostname + ":" + str(parsed_url.port)

    return {"https": url, "http": url}
