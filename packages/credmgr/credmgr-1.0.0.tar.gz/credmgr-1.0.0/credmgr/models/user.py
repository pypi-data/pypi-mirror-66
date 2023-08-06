from ..mixins import BaseModel, DeletableMixin, EditableMixin, ToggableMixin


class User(BaseModel, DeletableMixin, EditableMixin, ToggableMixin):
    _attrTypes = {
        **BaseModel._attrTypes,
        'id': 'int',
        'username': 'str',
        'is_active': 'bool',
        'is_regular_user': 'bool',
        'is_admin': 'bool',
        'default_settings': 'dict(str, str)',
        'reddit_username': 'str',
        'created': 'datetime',
        'updated': 'datetime'
    }

    _path = '/users'
    _credmgrCallable = 'user'
    _nameAttr = 'username'
    _enabledAttr = 'isActive'
    _canFetchByName = True
    _fetchNameAttr = _nameAttr

    def __init__(self, credmgr, id=None, username=None, isActive=None, isRegularUser=None, isAdmin=None, defaultSettings=None, redditUsername=None, created=None, updated=None):
        super().__init__(credmgr, id)
        if username:
            self.username = username
        if isActive is not None:
            self.isActive = isActive
        if isRegularUser is not None:
            self.isRegularUser = isRegularUser
        if isAdmin is not None:
            self.isAdmin = isAdmin
        if defaultSettings is not None:
            self.defaultSettings = defaultSettings
        if redditUsername is not None:
            self.redditUsername = redditUsername
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated

    @staticmethod
    def _create(_credmgr, username, password, defaultSettings=None, redditUsername=None, isAdmin=False, isActive=True, isRegularUser=True, isInternal=False):
        '''Create a new User

        **PERMISSIONS: Admin role is required.**

        :param str username: Username for new user (Example: ```spaz```) (required)
        :param str password: Password for new user (Example: ```supersecurepassword```) (required)
        :param str defaultSettings: Default values to use for new apps (Example: ```{"databaseFlavor": "postgres", "databaseHost": "localhost"}```)
        :param str redditUsername: User's Reddit username (Example: ```LilSpazJoekp```)
        :param bool isAdmin: Is the user an admin? Allows the user to see all objects and create users (Default: ``false``)
        :param bool isActive: Is the user active? Allows the user to sign in (Default: ``true``)
        :param bool isRegularUser: (Internal use only)
        :param bool isInternal: (Internal use only)
        :return: User

        '''
        additionalParams = {}
        if defaultSettings:
            additionalParams['default_settings'] = defaultSettings
        if isAdmin:
            additionalParams['is_admin'] = isAdmin
        if isActive:
            additionalParams['is_active'] = isActive
        if isRegularUser:
            additionalParams['is_regular_user'] = isRegularUser
        if isInternal:
            additionalParams['is_internal'] = isInternal
        if redditUsername:
            additionalParams['reddit_username'] = redditUsername
        return _credmgr.post('/users', data={'username': username, 'password': password, **additionalParams})