from typing import Any, Dict, Iterable, List, Tuple

from typing_extensions import Protocol

from ..utils.types import Collection, Event, FullQualifiedId, Headers


class AuthenticationProvider(Protocol):  # pragma: no cover
    """
    Interface for authentication adapter used in views.
    """

    def get_user(self, headers: Headers) -> int:
        ...


class PermissionProvier(Protocol):  # pragma: no cover
    """
    Interface for permission service used in views and actions.
    """

    def has_perm(self, user_id: int, permission: str) -> bool:
        ...


class DatabaseProvider(Protocol):  # pragma: no cover
    """
    Interface for database adapter used in views and actions.
    """

    def get(self, fqid: FullQualifiedId, mapped_fields: List[str] = None) -> None:
        ...

    def getMany(
        self, collection: Collection, ids: List[int], mapped_fields: List[str] = None
    ) -> Tuple[Dict[int, Dict[str, Any]], int]:
        ...

    def getId(self, collection: Collection) -> Tuple[int, int]:
        ...

    # def exists(self, collection: Collection, ids: List[int]) -> None: ...

    # getAll, filter, count, min, max, ...some with deleted or only deleted


class EventStoreProvider(Protocol):  # pragma: no cover
    """
    Interface for event store adapter used in views and actions.
    """

    def send(self, events: Iterable[Event]) -> None:
        ...
