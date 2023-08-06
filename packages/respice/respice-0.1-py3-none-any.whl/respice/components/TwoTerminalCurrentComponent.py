from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Hashable, Tuple, Sequence

import numpy as np

from .Branch import Branch, CurrentBranch
from .Component import Component


@dataclass(eq=False)
class TwoTerminalCurrentComponent(Component):
    """
    The base class for all two-terminal electrical components that have a voltage-to-current characteristic.

    This class avoids you to maintain `Branch`s for this simple two-terminal case. Instead of creating a branch,
    you can immediately override methods like `get_current` or `update` and access voltages and currents via this
    component itself (`component.v` and `component.i`).
    """
    _branch: TwoTerminalBranch = field(init=False)

    @dataclass(eq=False)
    class TwoTerminalBranch(CurrentBranch):
        """
        The branch that represents the two-terminal component.

        Effectively mirrors all functions like `get_current` back to the parent component.
        """
        component: TwoTerminalCurrentComponent

        def get_current(self, v_i: np.ndarray, dt: float) -> float:
            return self.component.get_current(v_i[0], dt)

        def get_jacobian(self, v_i: np.ndarray, dt: float) -> Sequence[float]:
            return [self.component.get_jacobian(v_i[0], dt)]

        def update(self, v: float, coupled_v: np.ndarray, dt: float):
            super().update(v, coupled_v, dt)

            self.component.update(v, dt)

    def __post_init__(self):
        self._branch = self.TwoTerminalBranch(self)

    def connect(self, terminal1: Hashable, terminal2: Hashable) -> List[Tuple[Hashable, Hashable, Branch]]:
        return [(terminal1, terminal2, self._branch)]

    @property
    def v(self) -> List[float]:
        """
        :return:
            The component's voltages calculated in a simulate step. Multiple simulations append their results to
            this field.
        """
        return self._branch.v

    @property
    def i(self) -> List[float]:
        """
        :return:
            The component's currents calculated in a simulate step. Multiple simulations append their results to
            this field.
        """
        return self._branch.i

    @property
    def p(self) -> List[float]:
        """
        :return:
            The component's power dissipation. Generates a new list calculated out of `self.v` and `self.i`, so this
            might be an expensive operation.
        """
        return self._branch.p

    def get_current(self, v: float, dt: float) -> float:
        """
        Calculated current depending on given voltage and time step.

        :param v:
            Voltage (measured in Volts).
        :param dt:
            Time step (measured in seconds).
        :return:
            The current (measured in Ampere).
        """
        raise NotImplementedError

    def get_jacobian(self, v: float, dt: float) -> float:
        """
        Returns the derivative (a.k.a. 1D Jacobian) of `get_voltage` over the voltage `v`.

        For the numerical algorithm to quickly converge with more accuracy, it is necessary for electrical circuit
        problems to supply the derivations of each current / voltage function.

        See also https://en.wikipedia.org/wiki/Derivative and
        https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant

        :param v:
            Voltage (measured in Volts).
        :param dt:
            Time step (measured in seconds). Note that dt / t (time) is not a variable to differentiate for in the
            Jacobi matrix.
        :return:
            The derivative value (measured in Ampere per second).
        """
        raise NotImplementedError

    def update(self, v: float, dt: float):
        """
        Updates the state of the element from the given voltage and time step.

        This method is called after each simulation cycle in the `Circuit.simulate` function.
        If the simulation algorithm was able to determine a proper voltage and current,
        this method is called to set those calculated values as the new "truth" for the
        next time step.

        :param v:
            New voltage (measured in Volts).
        :param dt:
            New time step (measured in seconds).
        """
        pass
