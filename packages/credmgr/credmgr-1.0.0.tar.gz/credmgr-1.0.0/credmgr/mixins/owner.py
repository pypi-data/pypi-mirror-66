from typing import TypeVar


User = TypeVar("User")
class OwnerMixin:
    _editableAttrs = []

    @property
    def owner(self) -> User:
        user = self._credmgr.user(id=self.ownerId)
        return user