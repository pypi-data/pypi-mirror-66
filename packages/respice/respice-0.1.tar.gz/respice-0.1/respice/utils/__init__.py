from respice.analysis import Circuit
from respice.components import Component


def create_series_connected_circuit(*components: Component) -> Circuit:
    """
    Utility to connect a closed circuit with all given elements connected in series.

    :param components:
        The elements to construct the circuit from.
    :return:
        A circuit.
    """
    if len(components) < 2:
        raise ValueError('Not enough elements to connect in series. At least 2 required.')

    circuit = Circuit()

    for i, elem in enumerate(components[:-1]):
        circuit.add(elem, i, i + 1)

    # Add closing element.
    circuit.add(components[-1], len(components) - 1, 0)

    return circuit


def plot_components(*components, dt: float, cycles: int):
    """
    Quick and dirty function to quickly plot components' voltages and currents in a circuit.

    You have to simulate the circuit beforehand. This function does not perform simulation!

    It's advisable to properly distinguish the components to give them names by assigning to their `name` field when
    adding them to the circuit.

    Uses matplotlib for plotting. So please install matplotlib before usage!

    :param components:
        The components to plot.
    :param dt:
        The time step used for prior simulation.
    :param cycles:
        The number of cycles used for prior simulation.
    """
    try:
        import matplotlib.pyplot as plot
    except ImportError:
        raise RuntimeError('matplotlib not found! Please install before using this function.')

    xvals = [dt * x for x in range(cycles)]

    legend = [c.name for c in components]

    plot.subplot(211)
    plot.grid()
    plot.xlabel('t [s]')
    plot.ylabel('V [V]')

    for component in components:
        plot.plot(xvals, component.v)
    plot.legend(legend)

    plot.subplot(212)
    plot.grid()
    plot.xlabel('t [s]')
    plot.ylabel('I [A]')

    for component in components:
        plot.plot(xvals, component.i)
    plot.legend(legend)

    plot.show()


def plot_circuit(circuit: Circuit, dt: float, cycles: int):
    """
    Quick and dirty function to quickly plot all components' voltages and currents in a circuit. Automatically
    performs the simulation with the given parameters.

    It's advisable to properly distinguish the components to give them names by assigning to their `name` field when
    adding them to the circuit.

    Uses matplotlib for plotting. So please install matplotlib before usage!

    :param circuit:
        The circuit to simulate and plot voltages and currents for.
    :param dt:
        The time step for simulation.
    :param cycles:
        The number of cycles for simulation.
    """
    try:
        import matplotlib.pyplot as plot
    except ImportError:
        raise RuntimeError('matplotlib not found! Please install before using this function.')

    circuit.simulate(dt, cycles)

    plot_components(*circuit.components, dt=dt, cycles=cycles)
