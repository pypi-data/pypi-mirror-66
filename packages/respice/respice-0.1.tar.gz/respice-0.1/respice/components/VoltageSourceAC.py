from dataclasses import dataclass, field
from math import sin, pi, sqrt

from respice.components import TwoTerminalVoltageComponent


@dataclass(eq=False)
class VoltageSourceAC(TwoTerminalVoltageComponent):
    """
    An AC current supply.

    You might alternatively set the current amplitude by specifying an effective voltage.
    Be sure to assign to the property `effective_amplitude` after initialization.

    amplitude:
        The current amplitude of the sine emitted by the supply (measured in Amperes).
    frequency:
        The current frequency (measured in Hertz).
    phase:
        The initial phase angle (measured in rad).
    """
    amplitude: float
    frequency: float
    phase: float = 0.0

    @property
    def effective_amplitude(self):
        """
        :return:
            The effective amplitude current (measured in Amperes).
        """
        return self.amplitude / sqrt(2)

    @effective_amplitude.setter
    def effective_amplitude(self, value: float):
        """
        Sets the amplitude of this supply via an effective value.

        This function just multiplies the given value with sqrt(2).

        :param value:
            The effective amplitude value.
        """
        self.amplitude = value * sqrt(2)

    _t: float = field(default=0.0, repr=False, init=False)

    def get_voltage(self, i: float, dt: float) -> float:
        return self.amplitude * sin((self._t + dt) * 2 * pi * self.frequency + self.phase)

    def get_jacobian(self, i: float, dt: float) -> float:
        return 0

    def update(self, i: float, dt: float):
        super().update(i, dt)

        self._t += dt
