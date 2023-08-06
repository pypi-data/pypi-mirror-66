import math
import warnings
from typing import Callable, Hashable, Dict, List

import numpy as np
from scipy.optimize import root, OptimizeResult

from respice.analysis.MNAEquationStack import MNAEquationStack
from respice.components import Branch, Component
from respice.components.Branch import CurrentBranch, VoltageBranch
from .UniqueEdgeMultiDiGraph import UniqueEdgeMultiDiGraph


class UnmetPrecisionWarning(UserWarning):
    def __init__(self, msg: str, result: OptimizeResult):
        super().__init__(msg)

        self.result = result


class Circuit:
    def __init__(self):
        self._graph = UniqueEdgeMultiDiGraph()

        # Enforces uniqueness of elements across all graph edges (additionally, since uniqueness is effectively already
        # enforced by the special MultiDiGraph type used, because same branches of components can't be added twice as
        # well). Since adding the same component twice would cause the data in its branches to become mixed up, since
        # multiple results get appended to the same branch instance.
        self._branches_to_components: Dict[Branch, Component] = {}
        self._components_to_branches: Dict[Component, List[Branch]] = {}

    def add(self, component: Component, *terminals: Hashable):
        """
        Adds a new component to the circuit.

        :param component:
            The component to connect.
        :param terminals:
            The nodes/potentials to connect the component to. See each component's documentation about the order of
            each terminal to be specified.
        """
        if component in self._components_to_branches:
            raise KeyError(f'given element at 0x{hex(id(component))} already added to circuit.')

        component_branches = component.connect(*terminals)

        self._components_to_branches[component] = [branch for _, _, branch in component_branches]

        for source, target, branch in component_branches:
            self._branches_to_components[branch] = component
            self._graph.add_edge(source, target, branch)

    def remove(self, component: Component):
        """
        Removes a component from the circuit.

        If the component does not exists, this function is a no-op.

        :param component:
            The component to remove from the circuit.
        """
        if component in self._components_to_branches:
            for branch in self._components_to_branches[component]:
                del self._branches_to_components[branch]
                self._graph.remove_edge(branch)

            del self._components_to_branches[component]

    @property
    def components(self):
        """
        :return:
            All components added to this circuit.
        """
        return self._components_to_branches.keys()

    def _get_coupled_branches(self, edge: Branch) -> List[Branch]:
        component = self._branches_to_components[edge]
        return self._components_to_branches[component]

    def _disturb_solution(self, trial: int, solution: OptimizeResult, factor_multiplier=100) -> np.ndarray:
        """
        Disturbs the result of a solution. This function is used when retrying the solution because convergence
        didn't succeed and has gotten so worse that the solver stops further trying. Trying with a different starting
        point is the recommended method.

        This function specifically applies relative disturbance and considers the direction of the Jacobian matrix
        to effectively over-shoot the current (non-converged) solution. The higher the trial number, the higher
        the overshooting.

        :param trial:
            The current trial number (starts from 1).
        :param solution:
            The `OptimizationResult` as received from `scipy.optimize.root`.
        :param factor_multiplier:
            The disturbance factor to the trial.
        :return:
            The disturbed solution vector.
        """
        directional_multiplier = np.array([(-1 if v < 0 else 1) for v in solution.fjac @ solution.x])
        return directional_multiplier * factor_multiplier**trial * solution.x

    def _solve(self, eq: Callable, dt: float, start_vector: np.ndarray, jac: None) -> OptimizeResult:
        """
        Attempts to solve the given electrical-circuit-governing system equation.

        Additionally employs retries if convergence tolerances are not reached with different starting points
        utilizing `_disturb_solution`. If `_disturb_solution` does yield conversion to the same (or rather very close
        point), then again a retry is attempted, but with a point that's more far away. If other points are hit that
        still don't fulfill convergence restrictions, retries are attempted on them as well. Retries are tracked per
        solution, so in case that we encounter cycles where we jump to different but non-satisfying solutions and come
        back to a solution we already had, `_disturb_solution` will attempt a different start vector never used before
        to not end up in useless wastes of trials.

        By default int((math.log10(len(start_vector)) + 1) * 4) trials will be attempted if needed, so for larger
        systems more points are investigated for bad convergence. To not increase evaluation time too much, the
        logarithm is used to only scale to the order of the system.

        :param eq:
            The system equation function to solve.
        :param dt:
            The time step.
        :param start_vector:
            The initial start vector.
        :param:
            The Jacobian (function) of eq.
        :return:
            The best found result to the system.
        """
        unsatisfying_results = []
        trials = {}
        retries = int((math.log10(len(start_vector)) + 1) * 4)
        for trial in range(retries):
            result = root(
                eq,
                start_vector,
                args=(dt,),
                method='hybr',
                jac=jac,
            )

            if result.success:
                break

            unsatisfying_results.append(result)

            # Result disturbance is a bit smarter and resets the trial count if we really found a different point,
            # so in case the next different value again does not converge, we do not overshoot extremely just because
            # this happened at a high trial count. However, if we might re-encounter the same solution, then the old
            # trial count gets restored again. That ensures that we really always try out new values and aren't driven
            # into useless re-evaluation of the same points until all trials are exhausted.
            for solution in trials:
                if math.isclose(np.linalg.norm(solution), np.linalg.norm(result.x)):
                    trials[solution] += 1
                    result_trials = trials[solution]
                    break
            else:
                trials[tuple(result.x)] = 1  # numpy arrays are not hashable, so we produce a hashable vector.
                result_trials = 1

            start_vector = self._disturb_solution(result_trials, result)
        else:
            # Filter out best result closest to zero.
            result = min(unsatisfying_results, key=lambda x: np.linalg.norm(x.fun))

            warnings.warn(UnmetPrecisionWarning(
                'Failed to converge after several retries. Taking the closest result as granted.',
                result,
            ))

        return result

    def simulate(self, dt: float, steps: int):
        """
        Perform a circuit simulation.

        Results can be accessed as voltages and currents in each element used in the given circuit
        (see documentation for `respice.components.Element`).

        Results are always appended to the previous simulation. This means you can chain simulations
        together altering parameters in between (for example turning off a voltage supply by removing
        it from the circuit or changing a resistance value).

        :param dt:
            The time step for each simulation cycle.
        :param steps:
            The number of cycles to simulate.
        """
        master_equation = MNAEquationStack(self._graph, self._components_to_branches.values())

        # Performance improvement: Lambdify equations by compiling a real Python expression out of them. This now
        # becomes a plain callable instead of having an evaluate() function.
        optimized_master_equation = master_equation.lambdify()
        optimized_jacobian = master_equation.lambdify_jacobian()

        start_vector = np.zeros(len(master_equation))
        for i in range(steps):
            result = self._solve(
                optimized_master_equation,
                dt,
                start_vector,
                jac=optimized_jacobian,
            ).x

            # Behaviour is usually smooth, so use the last result as a starting point for next evaluation.
            start_vector = result

            # Map back calculated voltages and currents to actual elements.
            for _, _, branch in self._graph.edges(keys=True):
                coupled_branches = self._get_coupled_branches(branch)

                coupled_v_i = []
                for coupled_branch in coupled_branches:
                    if isinstance(coupled_branch, CurrentBranch):
                        val = master_equation.get_voltage(result, coupled_branch)
                    elif isinstance(coupled_branch, VoltageBranch):
                        val = master_equation.get_current(result, coupled_branch)
                    else:
                        raise AssertionError(f'Unknown branch type encountered: f{type(coupled_branch)}')

                    coupled_v_i.append(val)

                coupled_v_i = np.array(coupled_v_i)

                if isinstance(branch, CurrentBranch):
                    branch.update(master_equation.get_voltage(result, branch), coupled_v_i, dt)
                elif isinstance(branch, VoltageBranch):
                    branch.update(master_equation.get_current(result, branch), coupled_v_i, dt)
                else:
                    raise AssertionError(f'Unknown branch type encountered: f{type(branch)}')
