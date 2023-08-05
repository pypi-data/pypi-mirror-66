from __future__ import annotations

from enum import IntEnum
from typing import Callable, Generic, List, Optional, Tuple, TypeVar

__all__ = ['Intent', 'actor', 'IntentMetaAction']


class IntentMetaAction(IntEnum):
    actor_added = 1
    actor_removed = 2
    all_actors_removed = 3
    deleted = 4
    announced = 5


T = TypeVar('T')
Actor = Callable[[T], None]
MetaT = Tuple[Optional[Actor[T]], Optional[T], IntentMetaAction]

F = TypeVar('F', bound=Callable)


def actor(func: F) -> F:
    return func


class Intent(Generic[T]):
    _actors: List[Actor[T]]
    _meta: Optional[Intent[MetaT]]

    def __init__(self) -> None:
        self._actors = []
        self._meta = None

    @property
    def meta(self) -> Intent[MetaT]:
        if self._meta is None:
            self._meta = Intent()
        return self._meta

    def subscribe(self, actor: Actor[T]) -> None:
        self._actors.append(actor)
        if self._meta is not None:
            self._meta.announce((actor, None, IntentMetaAction.actor_added))

    def unsubscribe(self, actor: Actor[T]) -> None:
        try:
            self._actors.remove(actor)
            if self._meta is not None:
                self._meta.announce((actor, None, IntentMetaAction.actor_removed))
        except ValueError:
            pass

    def unsubscribe_all(self) -> None:
        self._actors = []
        if self._meta is not None:
            self._meta.announce((None, None, IntentMetaAction.all_actors_removed))

    def announce(self, message: T) -> None:
        for sub in self._actors:
            sub(message)
        if self._meta is not None:
            self._meta.announce((None, message, IntentMetaAction.announced))

    def delete(self) -> None:
        if self._meta is not None:
            self._meta.announce((None, None, IntentMetaAction.deleted))
        self._actors = []
        if self._meta is not None:
            self._meta.delete()
