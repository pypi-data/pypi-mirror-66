
class OwnerMixin:
    _editableAttrs = []

    @property
    def owner(self):
        if self.ownerId is None:
            self.fetch()
        user = self._credmgr.user(id=self.ownerId)
        return user