from dataclasses import dataclass

from .TwoTerminalCurrentComponent import TwoTerminalCurrentComponent


@dataclass(eq=False)
class Inductance(TwoTerminalCurrentComponent):
    """
    Describes an ideal inductance (L*dI/dt = V)

    value:
        The inductance value in Henry.
    state_current:
        The momentary current. This is a state variable updated consecutively
        on each simulation iteration. However, you might set it ahead simulation
        to describe the inductance's initial state.
    state_voltage:
        The momentary voltage. Since this component uses the midpoint-method for
        calculation, this additional state variable is introduced for better accuracy.
        This is a state variable updated consecutively on each simulation iteration.
        However, you might set it ahead simulation to describe the inductance's initial state.
    """
    value: float

    state_current: float = 0.0
    state_voltage: float = 0.0

    def get_current(self, v: float, dt: float) -> float:
        return self.state_current + (self.state_voltage + v) / (2 * self.value) * dt

    def get_jacobian(self, v: float, dt: float) -> float:
        return dt / (2 * self.value)

    def update(self, v: float, dt: float):
        self.state_current = self.get_current(v, dt)
        self.state_voltage = v


L = Inductance
