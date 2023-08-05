# -*- coding: utf-8 -*-

import os
import tuxbuild.exceptions
from os.path import expanduser
import configparser
import requests
import time


class Config:
    def __init__(self, config_path="~/.config/tuxbuild/config.ini"):
        """
            Retrieve tuxbuild authentication token and API url

            Tuxbuild requires an API token. Optionally, a API url endpoint may
            be specified. The API url defaults to https://api.tuxbuild.com/v1.

            The token and url may be specified in environment variables, or in
            a tuxbuild config file. If using the config file, the environment
            variable TUXBUILD_ENV may be used to specify which tuxbuild config
            to use.

            Environment variables:
                TUXBUILD_TOKEN
                TUXBUILD_URL (optional)

            Config file:
                Must be located at ~/.config/tuxbuild/config.ini.
                This location can be overriden by setting the TUXBUILD_CONFIG
                environment variable.
                A minimum config file looks like:

                    [default]
                    token=vXXXXXXXYYYYYYYYYZZZZZZZZZZZZZZZZZZZg

                Multiple environments may be specified. The environment named
                in TUXBUILD_ENV will be chosen. If TUXBUILD_ENV is not set,
                'default' will be used.

                Fields:
                    token
                    api_url (optional)
        """

        self.default_api_url = (
            "https://api.tuxbuild.com/v1"  # Use production v1 if no url is specified
        )
        self.tuxbuild_env = os.getenv("TUXBUILD_ENV", "default")

        (self.auth_token, self.kbapi_url) = self._get_config_from_env()

        if os.getenv("TUXBUILD_CONFIG"):
            config_path = os.getenv("TUXBUILD_CONFIG")

        if not self.auth_token:
            (self.auth_token, self.kbapi_url) = self._get_config_from_config(
                config_path
            )

        if not self.auth_token:
            raise tuxbuild.exceptions.TokenNotFound(
                "Token not found in TUXBUILD_TOKEN nor at [{}] in {}".format(
                    self.tuxbuild_env, config_path
                )
            )
        if not self.kbapi_url:
            raise tuxbuild.exceptions.URLNotFound(
                "TUXBUILD_URL not set in env, or api_url not specified at [{}] in {}.".format(
                    self.tuxbuild_env, config_path
                )
            )

    def _get_config_from_config(self, config_path):
        path = expanduser(config_path)
        open(path, "r")  # ensure file exists and is readable
        config = configparser.ConfigParser()
        config.read(path)
        if not config.has_section(self.tuxbuild_env):
            raise configparser.NoSectionError(
                "Error, missing section [{}] from config file '{}'".format(
                    self.tuxbuild_env, path
                )
            )
        kbapi_url = (
            config[self.tuxbuild_env].get("api_url", self.default_api_url).rstrip("/")
        )
        auth_token = config[self.tuxbuild_env].get("token", None)
        return (auth_token, kbapi_url)

    def _get_config_from_env(self):
        # Check environment for TUXBUILD_TOKEN
        auth_token = None
        kbapi_url = None
        if os.getenv("TUXBUILD_TOKEN"):
            auth_token = os.getenv("TUXBUILD_TOKEN")
            kbapi_url = os.getenv("TUXBUILD_URL", self.default_api_url).rstrip("/")
        return (auth_token, kbapi_url)

    def get_auth_token(self):
        return self.auth_token

    def get_kbapi_url(self):
        return self.kbapi_url

    def get_tuxbuild_env(self):
        return self.tuxbuild_env

    def check_auth_token(self):
        headers = {"Content-type": "application/json", "Authorization": self.auth_token}
        url = self.kbapi_url + "/verify"
        attempts = 6
        for i in range(1, attempts + 1):
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return
            elif r.status_code // 500 == 1:
                if i < attempts:
                    time.sleep(2 ** i)  # exponential backoff
            else:
                r.raise_for_status()  # Some unexpected status that's not caught
