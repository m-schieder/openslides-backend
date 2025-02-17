from dataclasses import dataclass
from typing import Dict, List, Optional

from ..patterns import FullQualifiedId
from .collection_field_lock import CollectionFieldLock
from .event import Event

Information = Dict[FullQualifiedId, List[str]]


@dataclass
class WriteRequest:
    """
    Write request element that can be sent to the datastore.
    """

    events: List[Event]
    information: Information
    user_id: int
    locked_fields: Dict[str, CollectionFieldLock]
    migration_index: Optional[int] = None
