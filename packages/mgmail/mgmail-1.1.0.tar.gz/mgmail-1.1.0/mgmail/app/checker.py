import ssl
import requests
import imapclient
from imapclient import IMAPClient
"""
Checks if all connection points are ready
    1. Papermerge DMS - checks if it is possible to connect with given
    REST API key
    2. IMAP Server - checks if it sposible to connect at all
    3. SMTP account - checks if username/password combinations are valid
"""


class Checker():

    def __init__(self, config, logger):
        self.cfg = config
        self.logger = logger

    def run(self):
        self.checker_mg()
        self.checker_smtp()

    def checker_mg(self):
        papermerge_url = self.cfg.get('papermerge_url', False)
        api_key = self.cfg.get('api_key', False)

        if not papermerge_url:
            self.logger.error(
                "papermerge_url missing in config file"
            )
            return

        if not api_key:
            self.logger.error(
                "api_key missing in config file"
            )
            return

        url = f"{papermerge_url}/api/ping"
        headers = {
            'Authorization': f"Token {api_key}",
        }
        try:
            ret = requests.get(url, headers=headers)
            if ret.status_code != 200:
                self.logger.error(f"Check failed: {ret.reason}")

            self.logger.info(
                f"status: {ret.status_code}; reason: {ret.reason}"
            )
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Failed to connect to {papermerge_url}")
            return

        self.logger.info("MG connection OK")

    def checker_smtp(self):
        imap_server = self.cfg.get('imap_server', False)
        username = self.cfg.get('username', False)
        password = self.cfg.get('password', False)
        if not imap_server:
            self.logger.error(
                "imap_server key is missing in config file"
            )
            return
        if not username:
            self.logger.error(
                "username is missing in config file (smtp username)"
            )
            return
        if not password:
            self.logger.error(
                "password is missing in config file"
            )
            return
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        with IMAPClient(
            imap_server,
            ssl_context=ssl_context
        ) as server:
            try:
                server.login(username, password)
            except imapclient.exceptions.LoginError:
                self.logger.error(f"Failed to login to {imap_server}")
                return
            self.logger.info("IMAP login OK")
