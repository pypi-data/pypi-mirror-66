from dataclasses import dataclass, field
from math import sqrt, pi

from respice.math import fraction
from .TwoTerminalVoltageComponent import TwoTerminalVoltageComponent


@dataclass(eq=False)
class VoltageSourceRectangular(TwoTerminalVoltageComponent):
    """
    A rectangular voltage source supply.

    By default the voltage toggles between `+ amplitude / 2` and `- amplitude / 2`. To make
    the rectangular toggle between `0` and `amplitude`, use the `offset` field and set it
    to `amplitude / 2`.

    By default the duty cycle of the source is 0.5, meaning it toggles equally between min and max.
    The duty cycle determines how much time (relative) is spent between the min and max states.
    A value of 0 or below means the source becomes effectively a DC source serving constantly the minimum
    voltage. A value of 1 or above is effectively a constant DC source at maximum voltage.
    For example a value in between of 0.75 means that 75% of the period is spent at maximum voltage
    and the following 25% is minimum voltage.

    amplitude:
        The amplitude of the rectangular voltage (measured in Volts).
    frequency:
        The signal frequency (measured in Hertz).
    offset:
        The voltage offset of the signal (measured in Volts).
    phase:
        The phase angle (measured in rad).
    duty:
        The duty cycle. Meaningful values lie between 0 and 1.
    """
    amplitude: float
    frequency: float
    offset: float = 0.0
    phase: float = 0.0
    duty: float = 0.5

    @property
    def effective_amplitude(self):
        """
        :return:
            The effective amplitude voltage (measured in Volts).
        """
        return sqrt(self.amplitude ** 2 / 2.0 + 2 * self.offset ** 2)

    @effective_amplitude.setter
    def effective_amplitude(self, value: float):
        r"""
        Sets the amplitude of this supply via an effective value.

        The effective amplitude depends not only on the amplitude, but also on the offset.
        According to the formula for RMS (see https://en.wikipedia.org/wiki/Root_mean_square and
        https://en.wikipedia.org/wiki/RMS_amplitude)

        .. math:
            \sqrt{\frac{1}{T} \int_{0}^{T}{f(t)^2 dt}}

        one can derive the effective amplitude as

        .. math:
            f(t) &= \frac{\text{amplitude}}{2} + \text{offset}, 0 \leq t < \frac{1}{2}T \\
            f(t) &= -\frac{\text{amplitude}}{2} + \text{offset}, \frac{1}{2}T \leq t < T \\

        .. math:
            V_{\text{eff}} &= \sqrt{\frac{1}{2} \left( \frac{\text{amplitude}}{2} \cdot \text{offset} \right)^2 +
                \frac{1}{2} \left( \frac{-\text{amplitude}}{2} \cdot \text{offset} \right)^2} \\
            &= \sqrt{\frac{\text{amplitude}^2}{2} + 2 \cdot \text{offset}^2}

        Note that depending on the offset chosen, not all effective amplitudes are possible (except for offset = 0).

        :param value:
            The effective amplitude value.
        """
        try:
            self.amplitude = sqrt(2 * value ** 2 - 4 * self.offset ** 2)
        # Happens when the value inside the root turns negative, which means the given value is impossible.
        except ValueError:
            raise ValueError('impossible effective amplitude')

    _t: float = field(default=0.0, repr=False, init=False)

    def get_voltage(self, i: float, dt: float) -> float:
        high = fraction((self._t + dt) * self.frequency + self.phase / (2 * pi)) < self.duty
        return (self.amplitude * 0.5) * (1 if high else -1) + self.offset

    def get_jacobian(self, i: float, dt: float) -> float:
        return 0

    def update(self, v: float, dt: float):
        super().update(v, dt)
        self._t += dt
