"""
quantum circuit class
"""

from functools import partial
from typing import Tuple, List, Callable, Union, Optional

import numpy as np
import tensornetwork as tn
import graphviz

from . import gates
from .cons import npdtype, backend, contractor

Gate = gates.Gate


class Circuit:
    def __init__(self, nqubits: int) -> None:
        _prefix = "qb-"
        if nqubits < 2:
            raise ValueError(
                f"Number of qubits must be greater than 2 but is {nqubits}."
            )

        # Get nodes on the interior
        nodes = [
            tn.Node(
                np.array([[[1.0]], [[0,]]], dtype=npdtype), name=_prefix + str(x + 1),
            )
            for x in range(nqubits - 2)
        ]

        # Get nodes on the end
        nodes.insert(
            0, tn.Node(np.array([[1.0], [0,]], dtype=npdtype), name=_prefix + str(0),),
        )
        nodes.append(
            tn.Node(
                np.array([[1.0], [0,]], dtype=npdtype), name=_prefix + str(nqubits - 1),
            )
        )

        # Connect edges between middle nodes
        for i in range(1, nqubits - 2):
            tn.connect(nodes[i].get_edge(2), nodes[i + 1].get_edge(1))

        # Connect end nodes to the adjacent middle nodes
        if nqubits < 3:
            tn.connect(nodes[0].get_edge(1), nodes[1].get_edge(1))
        else:
            tn.connect(
                nodes[0].get_edge(1), nodes[1].get_edge(1)
            )  # something wrong here?
            tn.connect(nodes[-1].get_edge(1), nodes[-2].get_edge(2))

        self._nqubits = nqubits
        self._nodes = nodes
        self._front = [n.get_edge(0) for n in nodes]
        self._start = nodes
        self._meta_apply()
        self._qcode = ""
        self._qcode += str(self._nqubits) + "\n"

    def _meta_apply(self) -> None:
        sgates = ["i", "x", "y", "z", "h"] + ["cnot", "cz", "swap"] + ["toffoli"]
        for g in sgates:
            setattr(
                self,
                g,
                partial(self.apply_general_gate_delayed, getattr(gates, g), name=g),
            )
            setattr(
                self,
                g.upper(),
                partial(self.apply_general_gate_delayed, getattr(gates, g), name=g),
            )

        vgates = ["r"]
        for g in vgates:
            setattr(
                self,
                g,
                partial(
                    self.apply_general_variable_gate_delayed, getattr(gates, g), name=g
                ),
            )
            setattr(
                self,
                g.upper(),
                partial(
                    self.apply_general_variable_gate_delayed, getattr(gates, g), name=g
                ),
            )

    @classmethod
    def from_qcode(
        cls, qcode: str
    ) -> "Circuit":  # forward reference, see https://github.com/python/mypy/issues/3661
        """
        make circuit object from non universal simple assembly quantum language

        :param qcode:
        :return:
        """
        lines = [s for s in qcode.split("\n") if s.strip()]
        nqubits = int(lines[0])
        c = cls(nqubits)
        for l in lines[1:]:
            ls = [s for s in l.split(" ") if s.strip()]
            g = ls[0]
            index = []
            errloc = 0
            for i, s in enumerate(ls[1:]):
                try:
                    si = int(s)
                    index.append(si)
                except ValueError:
                    errloc = i + 1
                    break
            kwdict = {}
            if errloc > 0:
                for j, s in enumerate(ls[errloc::2]):
                    kwdict[s] = float(ls[2 * j + 1 + errloc])
            getattr(c, g)(*index, **kwdict)
        return c

    def to_qcode(self) -> str:
        return self._qcode

    def apply_single_gate(self, gate: Gate, index: int) -> None:
        gate.get_edge(0) ^ self._front[index]
        self._front[index] = gate.get_edge(1)
        self._nodes.append(gate)

    def apply_double_gate(self, gate: Gate, index1: int, index2: int) -> None:
        assert index1 != index2
        gate.get_edge(0) ^ self._front[index1]
        gate.get_edge(1) ^ self._front[index2]
        self._front[index1] = gate.get_edge(2)
        self._front[index2] = gate.get_edge(3)
        self._nodes.append(gate)

    def apply_general_gate(
        self, gate: Gate, *index: int, name: Optional[str] = None
    ) -> None:
        assert len(index) == len(set(index))
        noe = len(index)
        for i, ind in enumerate(index):
            gate.get_edge(i) ^ self._front[ind]
            self._front[ind] = gate.get_edge(i + noe)
        self._nodes.append(gate)
        if (
            name
        ):  # if no name is specified, then the corresponding op wont be recorded in qcode
            self._qcode += name + " "
            for i in index:
                self._qcode += str(i) + " "
            self._qcode = self._qcode[:-1] + "\n"

    apply = apply_general_gate

    def apply_general_gate_delayed(
        self, gatef: Callable[[], Gate], *index: int, name: Optional[str] = None
    ) -> None:
        gate = gatef()
        self.apply_general_gate(gate, *index, name=name)

    applyd = apply_general_gate_delayed

    def apply_general_variable_gate_delayed(
        self,
        gatef: Callable[..., Gate],
        *index: int,
        name: Optional[str] = None,
        **vars: float,
    ) -> None:
        gate = gatef(**vars)
        self.apply_general_gate(gate, *index, name=name)
        self._qcode = self._qcode[:-1] + " "  # rip off the final "\n"
        for k, v in vars.items():
            self._qcode += k + " " + str(v) + " "
        self._qcode = self._qcode[:-1] + "\n"

    def is_valid(self) -> bool:
        """
        [WIP], check whether the circuit is legal

        :return:
        """
        try:
            assert len(self._front) == self._nqubits
            for n in self._nodes:
                for e in n.get_all_dangling():
                    assert e in self._front
            return True
        except AssertionError:
            return False

    def _copy(self, conj: bool = False) -> Tuple[List[tn.Node], List[tn.Edge]]:
        """
        copy all nodes and dangling edges correspondingly

        :return:
        """
        ndict, edict = tn.copy(self._nodes, conjugate=conj)
        newnodes = []
        for n in self._nodes:
            newnodes.append(ndict[n])
        newfront = []
        for e in self._front:
            newfront.append(edict[e])
        return newnodes, newfront

    def wavefunction(self) -> tn.Node.tensor:
        nodes, d_edges = self._copy()
        t = contractor(nodes, output_edge_order=d_edges)
        return backend.reshape(t.tensor, shape=[1, -1])

    state = wavefunction

    def amplitude(self, l: str) -> tn.Node.tensor:
        assert len(l) == self._nqubits
        no, d_edges = self._copy()
        ms = []
        for i, s in enumerate(l):
            if s == "1":
                ms.append(
                    tn.Node(np.array([0, 1], dtype=npdtype), name=str(i) + "-measure")
                )
            elif s == "0":
                ms.append(
                    tn.Node(np.array([1, 0], dtype=npdtype), name=str(i) + "-measure")
                )
        for i, n in enumerate(l):
            d_edges[i] ^ ms[i].get_edge(0)

        no.extend(ms)
        return contractor(no).tensor

    def measure(self, *index: int, with_prob: bool = False) -> Tuple[str, float]:
        """

        :param index: measure on which quantum line
        :param with_prob: if true, theoretical probability is also returned
        :return:
        """
        # TODO: consideration on how to deal with measure in the middle of the circuit
        sample = ""
        p = 1
        for j in index:
            nodes1, edge1 = self._copy()
            nodes2, edge2 = self._copy(conj=True)
            for i, e in enumerate(edge1):
                if i != j:
                    e ^ edge2[i]
            for i in range(len(sample)):
                if sample[i] == "0":
                    m = np.array([1, 0], dtype=npdtype)
                else:
                    m = np.array([0, 1], dtype=npdtype)
                nodes1.append(tn.Node(m))
                nodes1[-1].get_edge(0) ^ edge1[index[i]]
                nodes2.append(tn.Node(m))
                nodes2[-1].get_edge(0) ^ edge2[index[i]]
            nodes1.extend(nodes2)
            rho = (
                1
                / p
                * contractor(nodes1, output_edge_order=[edge1[j], edge2[j]]).tensor
            )
            pu = rho[0, 0]
            r = np.random.rand()
            if r < pu:
                sample += "0"
                p = p * pu
            else:
                sample += "1"
                p = p * (1 - pu)
        if with_prob:
            return sample, p
        else:
            return sample, -1.0

    def perfect_sampling(self) -> Tuple[str, float]:
        """
        reference: arXiv:1201.3974.

        :return: sampled bit string and the corresponding theoretical probability
        """
        return self.measure(*[i for i in range(self._nqubits)], with_prob=True)

    def expectation(self, op: tn.Node, *index: int) -> tn.Node.tensor:
        nodes1, edge1 = self._copy()
        nodes2, edge2 = self._copy(conj=True)
        noe = len(index)
        for j, e in enumerate(index):
            edge1[e] ^ op.get_edge(j)
            edge2[e] ^ op.get_edge(j + noe)
        for j in range(self._nqubits):
            if j not in index:  # edge1[j].is_dangling invalid here!
                edge1[j] ^ edge2[j]
        nodes1.append(op)
        nodes1.extend(nodes2)
        # self._nodes = nodes1
        return contractor(nodes1).tensor

    def to_graphviz(
        self,
        graph: graphviz.Graph = None,
        include_all_names: bool = False,
        engine: str = "neato",
    ) -> graphviz.Graph:
        """
        Not an ideal visualization for quantum circuit, but reserve here as a general approch to show tensornetwork

        :param graph:
        :param include_all_names:
        :param engine:
        :return:
        """
        # Modified from tensornetwork codebase
        nodes = self._nodes
        if graph is None:
            # pylint: disable=no-member
            graph = graphviz.Graph("G", engine=engine)
        for node in nodes:
            if not node.name.startswith("__") or include_all_names:
                label = node.name
            else:
                label = ""
            graph.node(str(id(node)), label=label)
        seen_edges = set()
        for node in nodes:
            for i, edge in enumerate(node.edges):
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                if not edge.name.startswith("__") or include_all_names:
                    edge_label = edge.name + ": " + str(edge.dimension)
                else:
                    edge_label = ""
                if edge.is_dangling():
                    # We need to create an invisible node for the dangling edge
                    # to connect to.
                    graph.node(
                        "{}_{}".format(str(id(node)), i),
                        label="",
                        _attributes={"style": "invis"},
                    )
                    graph.edge(
                        "{}_{}".format(str(id(node)), i),
                        str(id(node)),
                        label=edge_label,
                    )
                else:
                    graph.edge(
                        str(id(edge.node1)), str(id(edge.node2)), label=edge_label,
                    )
        return graph
