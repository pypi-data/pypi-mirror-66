from urllib.parse import urljoin

from requests import Session

from . import models
from .auth import ApiTokenAuth
from .exceptions import InitializationError
from .requestor import Requestor
from .serializer import Serializer


User = models.User
Bot = models.Bot
RedditApp = models.RedditApp
RefreshToken = models.RefreshToken
UserVerification = models.UserVerification
SentryToken = models.SentryToken
DatabaseCredential = models.DatabaseCredential

def setOwner(ownerId, data):
    if ownerId:
        data['ownerId'] = ownerId

class CredentialManager(object):
    '''The CredentialManager class provides convenient access to CredentialManager's API.

    Instances of this class are the gateway to interacting with CredentialManager's API
    through CredentialManager. The canonical way to obtain an instance of this class is via:


    .. code-block:: python

        import CredentialManager
        credmgr = CredentialManager.client(apiToken='LIqbGjAeep3Ws5DH3LOEQPmw8UZ6ek')


    '''
    _default = None
    _endpoint = '/api/v1'

    def __init__(self, host='https://credmgr.jesassn.org', apiToken=None, username=None, password=None, sessionClass=None, sessionKwargs={}):
        '''Initialize a CredentialManager instance.

        :param str host: Hostname to use for interacting with the API (default: ``https://credmgr.jesassn.org``)
        :param str apiToken: API Token used for authentication (Note: cannot be used when ``username`` and ``password`` params are passed)
        :param str username: Username to use for interacting with the API (Note: Cannot be used when ``apiToken`` param is passed)
        :param str password: Password to use for interacting with the API (Note: Cannot be used when ``apiToken`` param is passed)
        :param Session sessionClass: A Session class that will be used to create a requestor. If not set, use ``requests.Session`` (default: None).
        :param dict sessionKwargs: Dictionary with additional keyword arguments used to initialize the session (default: None).

        .. warning::
             Using an API Token instead of a username/password is strongly recommended!

        The ``sessionClass`` and ``sessionKwargs`` allow for
        customization of the session :class:`.CredentialManager` will use. This allows,
        e.g., easily adding behavior to the requestor or wrapping its
        |Session|_ in a caching layer. Example usage:

        .. |Session| replace:: ``Session``
        .. _Session: https://2.python-requests.org/en/master/api/#requests.Session

        .. code-block:: python

           import json, betamax, requests

           class JSONDebugRequestor(Requestor):
               def request(self, *args, **kwargs):
                   response = super().request(*args, **kwargs)
                   print(json.dumps(response.json(), indent=4))
                   return response

           mySession = betamax.Betamax(requests.Session())
           reddit = CredentialManager.client(..., sessionClass=JSONDebugRequestor, sessionKwargs={'session': mySession})
        '''
        self._host = urljoin(host, self._endpoint)
        if all([apiToken, username, password]):
            raise InitializationError('Either apiToken or username/password pair can be passed, both cannot be passed')
        if apiToken:
            self._auth = ApiTokenAuth(apiToken)
        elif username and password:
            self._auth = (username, password)
        else:
            raise InitializationError('apiToken or an username/password pair must be passed')

        self._requestor = Requestor(self._host, self._auth, sessionClass, **sessionKwargs)
        self.serializer = Serializer(self)
        self.currentUser: User = self.currentUser()
        self.userDefaults = self.currentUser.defaultSettings
        self.getUserDefault = lambda key, default: self.userDefaults.get(key, default)
        self.user = models.UserHelper(self)
        '''An instance of :class:`.UserHelper`.

        Provides the interface for interacting with :class:`.User`.
        For example to get a ``user`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            user = credmgr.user(1)
            print(user.id)
        
        To create a ``user`` do:
        
        ..code-block:: python
            user = credmgr.user.create(**userKwargs)
        
        See :meth:`~.UserHelper.create` for the required params.
        '''
        self.bot = models.BotHelper(self)
        '''An instance of :class:`.BotHelper`.

        Provides the interface for interacting with :class:`.Bot`.
        For example to get a ``bot`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            bot = credmgr.bot(1)
            print(bot.id)
        
        To create a ``bot`` do:
        
        ..code-block:: python
            bot = credmgr.bot.create(**botKwargs)
        
        See :meth:`~.BotHelper.create` for the required params.
        '''

        self.redditApp = models.RedditAppHelper(self)
        '''An instance of :class:`.RedditAppHelper`.

        Provides the interface for interacting with :class:`.RedditApp`.
        For example to get a ``redditApp`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            redditApp = credmgr.redditApp(1)
            print(redditApp.id)
        
        To create a ``redditApp`` do:
        
        ..code-block:: python
            redditApp = credmgr.redditApp.create(**redditAppKwargs)
        
        See :meth:`~.RedditAppHelper.create` for the required params.
        '''

        self.refreshToken = models.RefreshTokenHelper(self)
        '''An instance of :class:`.RefreshTokenHelper`.

        Provides the interface for interacting with :class:`.RefreshToken`.
        For example to get a ``refreshToken`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            refreshToken = credmgr.refreshToken(1)
            print(refreshToken.id)
        
        .. note::
            Refresh tokens cannot be manually created.
        '''

        self.userVerification = models.UserVerificationHelper(self)
        '''An instance of :class:`.UserVerificationHelper`.

        Provides the interface for interacting with :class:`.UserVerification`.
        For example to get a ``userVerification`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            userVerification = credmgr.userVerification(1)
            print(userVerification.id)
        
        To create a ``userVerification`` do:
        
        ..code-block:: python
            userVerification = credmgr.userVerification.create(**userVerificationKwargs)
        
        See :meth:`~.UserVerificationHelper.create` for the required params.
        '''

        self.sentryToken = models.SentryTokenHelper(self)
        '''An instance of :class:`.SentryTokenHelper`.

        Provides the interface for interacting with :class:`.SentryToken`.
        For example to get a ``sentryToken`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            sentryToken = credmgr.sentryToken(1)
            print(sentryToken.id)
        
        To create a ``sentryToken`` do:
        
        ..code-block:: python
            sentryToken = credmgr.sentryToken.create(**sentryTokenKwargs)
        
        See :meth:`~.SentryTokenHelper.create` for the required params.
        '''

        self.databaseCredential = models.DatabaseCredentialHelper(self)
        '''An instance of :class:`.DatabaseCredentialHelper`.

        Provides the interface for interacting with :class:`.DatabaseCredential`.
        For example to get a ``databaseCredential`` with ``id`` of ``1`` do:
        
        .. code-block:: python
            databaseCredential = credmgr.databaseCredential(1)
            print(databaseCredential.id)
        
        To create a ``databaseCredential`` do:
        
        ..code-block:: python
            databaseCredential = credmgr.databaseCredential.create(**databaseCredentialKwargs)
        
        See :meth:`~.DatabaseCredentialHelper.create` for the required params.
        '''

    def users(self, batchSize=10, limit=None):
        return User(self).listItems(batchSize=batchSize, limit=limit)

    def bots(self, batchSize=20, limit=None, owner=None):
        return Bot(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def redditApps(self, batchSize=20, limit=None, owner=None):
        return RedditApp(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def refreshTokens(self, batchSize=20, limit=None, owner=None):
        return RefreshToken(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def userVerifications(self, batchSize=20, limit=None, owner=None):
        return UserVerification(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def sentryTokens(self, batchSize=20, limit=None, owner=None):
        return SentryToken(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def databaseCredentials(self, batchSize=20, limit=None, owner=None):
        return DatabaseCredential(self).listItems(batchSize=batchSize, limit=limit, owner=owner)

    def currentUser(self) -> User:
        return self.get('/users/me')

    def get(self, path, params=None):
        return self.serializer.deserialize(self._requestor.request(path, 'GET', params=params))

    def post(self, path, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self.serializer.deserialize(self._requestor.request(path, 'POST', data=data, headers=headers))

    def patch(self, path, data):
        return self.serializer.deserialize(self._requestor.request(path, 'PATCH', json=data))

    def delete(self, path):
        return self._requestor.request(path, 'DELETE')