"""Simulation module.

This module contains the Simulation base class.
"""

# Standard library imports
from typing import Union

# Local application imports
from simplesim import base


class Simulation(base.Observable):
    """Base simulation class.

    """
    def __init__(self, start_time: Union[int, float] = 0,
                 d_time: Union[int, float] = 1) -> None:
        """Simulation initialization function.

        :param start_time: simulation start time
        :param d_time: simulation time step
        """
        super(Simulation, self).__init__()
        self._current_time = start_time
        self._delta_time = d_time

    @property
    def current_time(self) -> Union[int, float]:
        """Get current simulation time.

        :return: current simulation time
        """
        return self._current_time

    @current_time.setter
    def current_time(self, value: Union[int, float]) -> None:
        """Set current simulation time.

        :param value: new simulation time
        :return: None
        """
        self._current_time = value

    @property
    def delta_time(self) -> Union[int, float]:
        """Get simulation time delta.

        :return: simulation time delta
        """
        return self._delta_time

    @delta_time.setter
    def delta_time(self, value: Union[int, float]) -> None:
        """Set simulation time delta

        :param value: new simulation time delta
        :return: None
        """
        self._delta_time = value

    def step(self) -> None:
        """Increment the simulation.

        Increments the simulation time by time delta and updates
        observers.

        :return: None
        """
        self._current_time += self._delta_time

        for observer in self._observers:
            observer.update(time=self._current_time)

    def run(self, steps: int) -> None:
        """Run simulation for specified number of steps.

        :param steps: number of steps to run
        :return: None
        """
        for _ in range(0, steps):
            self.step()
