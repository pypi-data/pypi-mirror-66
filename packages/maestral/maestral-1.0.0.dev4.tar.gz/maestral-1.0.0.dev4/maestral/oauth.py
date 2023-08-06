# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under the MIT licence.

This module is responsible for authorization and token store in the system keyring.

"""

# system imports
import logging

# external imports
import click
import keyring.backends
import keyrings.alt
from keyring.core import load_keyring
from keyring.errors import KeyringLocked
import requests
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

# local imports
from maestral.config import MaestralConfig
from maestral.constants import DROPBOX_APP_KEY
from maestral.client import CONNECTION_ERRORS
from maestral.errors import KeyringAccessError


logger = logging.getLogger(__name__)

supported_keyring_backends = (
    keyring.backends.OS_X.Keyring,
    keyring.backends.SecretService.Keyring,
    keyring.backends.kwallet.DBusKeyring,
    keyring.backends.kwallet.DBusKeyringKWallet4,
    keyrings.alt.file.PlaintextKeyring
)


def get_keyring_backend(config_name):
    """
    Choose the most secure of the available and supported keyring backends or
    use the backend specified in the config file (if valid).

    :param str config_name: The config name.
    """

    import keyring.backends

    conf = MaestralConfig(config_name)
    keyring_class = conf.get('app', 'keyring').strip()

    try:
        ring = load_keyring(keyring_class)
    except Exception:
        # get preferred keyring backends for platform
        available_rings = keyring.backend.get_all_keyring()
        supported_rings = [k for k in available_rings
                           if isinstance(k, supported_keyring_backends)]

        ring = max(supported_rings, key=lambda x: x.priority)

    return ring


class OAuth2Session:
    """
    OAuth2Session provides OAuth 2 login and token store in the preferred system kering.
    To authenticate with Dropbox, run :meth:`get_auth_url`` first and direct the user to
    visit that URL and retrieve an auth token. Verify the provided auth token with
    :meth:`verify_auth_token` and save it in the system keyring together with the
    corresponding Dropbox ID by calling :meth:`save_creds`.

    This will currently use PKCE if available and fall back to the implicit grant flow
    implemented in :mod:`utils.oauth_implicit` otherwise.

    :param str config_name: Name of maestral config.

    :cvar int Success: Exit code for successful auth.
    :cvar int InvalidToken: Exit code for invalid token.
    :cvar int ConnectionFailed: Exit code for connection errors.
    """

    Success = 0
    InvalidToken = 1
    ConnectionFailed = 2

    def __init__(self, config_name, app_key=DROPBOX_APP_KEY):

        self._app_key = app_key

        self.keyring = get_keyring_backend(config_name)
        self._conf = MaestralConfig(config_name)

        self._auth_flow = DropboxOAuth2FlowNoRedirect(self._app_key, use_pkce=True)
        self._oAuth2FlowResult = None

        self._access_token = None

    @property
    def account_id(self):
        return self._conf.get('account', 'account_id')

    @account_id.setter
    def account_id(self, account_id):
        self._conf.set('account', 'account_id', account_id)

    @property
    def access_token(self):
        # defer keyring access until token requested by user
        if self._access_token is None:
            self._access_token = self.load_token()
        return self._access_token

    def load_token(self):
        """
        Load auth token from system keyring.

        :returns: Auth token.
        :rtype: str
        :raises: :class:`keyring.errors.KeyringLocked` if the system keyring is locked.
        """
        logger.debug(f'Using keyring: {self.keyring}')

        try:
            if self.account_id == '':
                self._access_token = ''
            else:
                token = self.keyring.get_password('Maestral', self.account_id)
                self._access_token = '' if token is None else token
            return self._access_token
        except KeyringLocked:
            info = f'Could not load access token. {self.keyring.name} is locked.'
            logger.error(info)
            raise KeyringAccessError('Could not load access token',
                                     f'{self.keyring.name} is locked.')

    def get_auth_url(self):
        """
        Gets the auth URL to start the OAuth2 implicit grant flow.

        :returns: Dropbox auth URL.
        :rtype: str
        """
        authorize_url = self._auth_flow.start()
        return authorize_url

    def verify_auth_token(self, token):
        """
        Verify the provided authorization token with Dropbox servers.

        :returns: :attr:`Success`, :attr:`InvalidToken`, or :attr:`ConnectionFailed`.
        :rtype: int
        :raises: :class:`errors.DropboxAuthError`
        """

        try:
            self._oAuth2FlowResult = self._auth_flow.finish(token)
            self._access_token = self._oAuth2FlowResult.access_token
            self.account_id = self._oAuth2FlowResult.account_id
            return self.Success
        except requests.exceptions.HTTPError:
            return self.InvalidToken
        except CONNECTION_ERRORS:
            return self.ConnectionFailed

    def save_creds(self):
        """Saves auth key to system keyring."""
        self._conf.set('account', 'account_id', self.account_id)
        try:
            self.keyring.set_password('Maestral', self.account_id, self.access_token)
            click.echo(' > Credentials written.')
            if isinstance(self.keyring, keyrings.alt.file.PlaintextKeyring):
                click.echo(' > Warning: No supported keyring found, '
                           'Dropbox credentials stored in plain text.')
        except KeyringLocked:
            # fall back to plain text keyring and try again
            self.keyring = keyrings.alt.file.PlaintextKeyring()
            self._conf.set('app', 'keyring', 'keyrings.alt.file.PlaintextKeyring')
            self.save_creds()

    def delete_creds(self):
        """Deletes auth key from system keyring."""
        try:
            self.keyring.delete_password('Maestral', self.account_id)
            click.echo(' > Credentials removed.')
        except KeyringLocked:
            info = f'Could not delete access token. {self.keyring.name} is locked.'
            logger.error(info)
            raise KeyringAccessError('Could not delete access token',
                                     f'{self.keyring.name} is locked.')
        finally:
            self._conf.set('account', 'account_id', '')
