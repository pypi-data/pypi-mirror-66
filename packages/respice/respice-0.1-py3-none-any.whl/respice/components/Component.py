from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Hashable, Tuple

from .Branch import Branch


@dataclass(eq=False)
class Component:
    """
    The base class for all electrical components.

    Each component consists of at least one `Edge`. An edge represents a potential difference between two terminals.
    Since a component can be multi-terminal, it must itself specify what edges are created between a given amount
    of terminal by the user. Those terminals are passed in order to the `connect` function. See `connect()`.

    name:
        An optional name to set for the component. Can be set after initialization.
    """
    name: str = field(default=None, init=False)

    def connect(self, *terminals: Hashable) -> List[Tuple[Hashable, Hashable, Branch]]:
        """
        Specifies how the component gets connected in the underlying circuit graph representation.

        When calling `circuit.add_element`, the order of the terminals specified matters. The elements `connect`
        function is called with the terminals to connect with in order. This function shall establish edges in the
        graph representation of the circuit and add so called "couplings". Couplings are equations that further
        constraint the behaviour between different edges (or the behaviour on the edge itself, then the element
        is "self-coupled").

        For example:
        - A resistance is a self-coupled element. Its current is immediately depending on its voltage.
        - A coupled inductance is a mutually-coupled element. Its current depends on the voltage of the other side
          and vice versa. The edges describing the two coils on each side are mutually coupled by one
          additional equation each.

        :param graph:
            The graph to establish edges/connections in.
        :param terminals:
            The potentials (aka terminals) to connect the element's ports with.
        :return:
            A list of edges in the form of `(terminal1, terminal2, edge)`. The order is respected in the voltage-vector
            when invoking each edge's `get_current` function.
        """
        raise NotImplementedError("I don't know how to connect this element between the given terminals")
