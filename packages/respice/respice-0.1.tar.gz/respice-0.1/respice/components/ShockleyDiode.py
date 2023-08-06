from math import exp

from dataclasses import dataclass

from .TwoTerminalCurrentComponent import TwoTerminalCurrentComponent


@dataclass(eq=False)
class ShockleyDiode(TwoTerminalCurrentComponent):
    """
    Describes an ideal Schockley Diode backed by the ideal Schockley equation.

    See https://en.wikipedia.org/wiki/Diode_modelling#Shockley_diode_model

    i_s:
        Reverse bias saturation current (also known as leakage current). Usually in the magnitudes of 10^-12 A.
    v_t:
        Thermal voltage V_T. For approximate room temperate 300K this value
        is 25.85mV (0.02585V). This is default.
    n:
        Ideality factor (also known as quality factor). By default 1.
    """
    i_s: float
    v_t: float = 0.02585
    n: float = 1.0

    def get_current(self, v: float, dt: float) -> float:
        return self.i_s * (exp(v / (self.n * self.v_t)) - 1)

    def get_jacobian(self, v: float, dt: float) -> float:
        return self.i_s / (self.n * self.v_t) * exp(v / (self.n * self.v_t))
