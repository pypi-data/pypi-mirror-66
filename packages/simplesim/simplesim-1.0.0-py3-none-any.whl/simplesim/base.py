"""Base class module.

This module contains base definitions used elsewhere in the package.
"""

# Standard library imports
from typing import Any
from typing import List


# pylint: disable=too-few-public-methods
class Observer:
    """Observer base class.

    Implements the observer object pattern. Children should override
    the update method.
    """
    def update(self, **kwargs: Any) -> None:
        """Update the observer to some event.

        :param kwargs: dict of various arguments.
        :return: None
        """


class Observable:
    """Observable base class.

    Implements the observable object pattern.
    """
    def __init__(self) -> None:
        """Observable initialization method.

        """
        self._observers = []

    @property
    def observers(self) -> List[Observer]:
        """Get list of observers

        :return: list of observers
        """
        return self._observers

    def add_observer(self, observer: Observer) -> None:
        """Add an observer to the list of observers.

        :param observer: observer to add
        :return: None
        """
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the list of observers.

        :param observer: observer to remove
        :return: None
        """
        self._observers.remove(observer)

    def notify(self, **kwargs: Any) -> None:
        """Notify observers of an update.

        :return: None
        """
        for observer in self._observers:
            observer.update(**kwargs)
