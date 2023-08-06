from dataclasses import dataclass

from .TwoTerminalVoltageComponent import TwoTerminalVoltageComponent


@dataclass(eq=False)
class Capacitance(TwoTerminalVoltageComponent):
    """
    Represents an ideal capacitance.

    value:
        The capacitance value (measured in Farad).
    state_voltage:
        The momentary voltage. This is a state variable updated consecutively
        on each simulation iteration. However, you might set it ahead simulation
        to describe the capacitance's initial state.
    state_current:
        The momentary current. Since this component uses the midpoint-method for
        calculation, this additional state variable is introduced for better accuracy.
        This is a state variable updated consecutively on each simulation iteration.
        However, you might set it ahead simulation to describe the capacitance's initial state.
    """
    value: float

    state_voltage: float = 0.0
    state_current: float = 0.0

    def get_voltage(self, i: float, dt: float) -> float:
        return self.state_voltage + (self.state_current + i) / (2 * self.value) * dt

    def get_jacobian(self, i: float, dt: float) -> float:
        return dt / (2 * self.value)

    def update(self, i: float, dt: float):
        self.state_voltage = self.get_voltage(i, dt)
        self.state_current = i


C = Capacitance
