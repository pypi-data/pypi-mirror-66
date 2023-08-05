import logging
from datetime import datetime
from typing import Optional
from .credentials_parser import resolve_credentials

from authlib.integrations.requests_client import OAuth2Session

DEFAULT_HOST = "https://user.annotell.com"

log = logging.getLogger(__name__)

# https://docs.authlib.org/en/latest/client/oauth2.html
class AuthSession:
    """
    Not thread safe
    """
    def __init__(self, *,
                 auth=None,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 host: str = DEFAULT_HOST):
        """
        There is a variety of ways to setup the authentication. See
        https://github.com/annotell/annotell-python/tree/master/annotell-auth
        :param auth: authentication credentials
        :param client_id: client id for authentication
        :param client_secret: client secret for authentication
        :param host: base url for authentication server
        """
        self.host = host
        self.token_url = "%s/v1/auth/oauth/token" % self.host

        client_id, client_secret = resolve_credentials(auth, client_id, client_secret)

        self.oauth_session = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
            token_endpoint_auth_method='client_secret_post',
            update_token=self._update_token,
            token_endpoint=self.token_url
        )

        self._token = None
        self._expires_at = None

    def _log_new_token(self):
        log.info(f"Got new token, with ttl={self._token['expires_in']} and expires {self._expires_at} UTC")

    def _update_token(self, token, access_token=None, refresh_token=None):
        self._token = token
        self._log_new_token()

    def init(self):
        # maybe support loading from file?
        # for now, just fetch a new token
        self.fetch_token()

    def fetch_token(self):
        log.debug("Fetching token")
        self._token = self.oauth_session.fetch_access_token(url=self.token_url)
        self._expires_at = datetime.utcfromtimestamp(self._token['expires_at'])
        self._log_new_token()

    @property
    def token(self):
        return self._token

    @property
    def access_token(self):
        return self._token.get('access_token') if self._token is not None else None

    @property
    def session(self):
        if not self._token:
            self.init()
        return self.oauth_session.session


