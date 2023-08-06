"""Allows users to enter shorthand for ID or Handle and have it *just work*"""
import abc
from typing import Set
from uuid import UUID

import attr

from hackgame.models import ObjectType


@attr.s(auto_attribs=True, frozen=True)
class CacheItem:
    public_uuid: UUID
    handle: str
    object_type: ObjectType
    added_at: int


class IdentifierCache(abc.ABC):
    """A cache of Identifier/Handle pairs the user has seen in responses"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def lookup(self, start: str, object_type=None) -> Set[CacheItem]:
        ...

    def store(self, item: CacheItem):
        pass


class ShelfIdentifierCache(IdentifierCache):
    def __init__(self, shelf: dict):
        """Either a Shelf object or a dict contained within one"""
        super().__init__()
        self._shelf = shelf
        if "items" not in self._shelf:
            self._shelf["items"] = set()
        self._shelf["items"]: Set[CacheItem]

    def lookup(self, start: str, object_type=None) -> Set[CacheItem]:
        """For the start of an Identifier, return any CacheItems that match"""
        candidates = set()
        for item in self._shelf["items"]:

            same_type = object_type and object_type == item.object_type

            if same_type and str(item.public_uuid).startswith(start):
                candidates.add(item)
            elif same_type and item.handle.startswith(start):
                candidates.add(item)
        return candidates

    def store(self, item: CacheItem) -> None:
        self._shelf["items"].add(item)
