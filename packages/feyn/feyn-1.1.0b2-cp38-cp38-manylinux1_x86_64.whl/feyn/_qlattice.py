import os
import typing

import requests

import _feyn
from feyn import Graph, QGraph

from ._register import Register


class QLattice:
    """
    A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction.

    The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

    The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communcate with, extract models from, and update the QLattice.

    The workflow is typically:
    1) extract a QGraph from the QLattice using `QLattice.get_qgraph`.
    2) fit the QGraph to a local dataset using `QGraph.fit`.
    3) select one or more models from the QGraph using `QGraph.select`.
    4) potentially update the QLattice with new knowledge using `QLattice.update`.

    Arguments:
        url -- URL of your QLattice.
        api_token -- Authentication token for the communicating with this QLattice.
    """

    _QLATTICE_BASE_URI = os.environ.get('QLATTICE_BASE_URI') or 'http://localhost:5000'

    def __init__(self, url: str=None, api_token: str=None) -> None:
        """Construct a new 'QLattice' object."""
        if url is None:
            url = self._QLATTICE_BASE_URI

        if '/api/v1/qlattice' not in url:
            url += "/api/v1/qlattice"

        self.url = url

        if api_token == None:
            api_token = os.environ.get('FEYN_TOKEN', "none")

        self.headers = {
            'Authorization': f'Bearer {api_token}'
        }

        self._load_qlattice()

    def get_register(self, label: str, register_type: str = "fixed") -> Register:
        """
        Get a reference to a QLattice `Register`. If the register doesn't exist, allocate a new one.

        Before you can extract a QGraph from the QLattice, you need to allocate a register for each input feature and the output feature you want to predict.

        The registers serve as the input and output points into a QLattice and must be specified when extracting QGraphs from the QLattice.

        For example, allocating registers for each column in a pandas dataframe can be done like this:

        # Allocate registers for all columns
        >>> output_reg = ql.get_register("target")
        >>> input_regs = []
        >>> for colname in df.columns:
        >>>     if colname != "target":
        >>>         input_regs.append(ql.get_register(colname))

        There are two different types of registers: "fixed" registers which assume that the input values are numerical, and "cat" registers which assume that the input values are distinct values such as labels or classes, where each distict value has it's own weight.

        Note: You cannot use a "cat" register as an output register.

        Arguments:
            label -- Name of the register.
            register_type -- Register type, either "fixed" or "cat". (numerical or categorical).
        Returns:
            Register -- The register instance.
        """
        if register_type not in ["fixed", "cat"]:
            raise ValueError("register_type must be 'fixed' or 'cat'.")

        req = requests.put("%s/register" % self.url,
                            headers=self.headers,
                            json={
                                'celltype': register_type,
                                'label': label
                            })
        req.raise_for_status()

        if req.status_code == 200:
            self._load_qlattice()

        reg = req.json()

        res = Register(register_type, reg['label'], reg['location'])

        return res

    def get_qgraph(self, inputs: typing.List[Register], output: Register, max_depth: int = 5) -> QGraph:
        """
        Extract QGraph from inputs registers to an output register.

        The standard workflow for QLattices is to extract a QGraph using this function. You specify a list of input registers corresponding to the input values you want to use for predictions, and a single output register corresponding to the output variable you want to predict.

        Once the QGraph has been extracted from the QLattice, you'll typically use the `QGraph.fit()` function to fit the QGraph to an actual dataset, and then `QGraph.select()` to select the final model.

        Arguments:
            inputs -- List of input registers.
            output -- The output register.
            max_depth -- The maximum depth of the graphs.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """
        req = requests.post("%s/simulation" % self.url,
                            headers=self.headers,
                            json={
                                'inputs': [reg.to_dict() for reg in inputs],
                                'output': output.to_dict(),
                                'max_depth': max_depth
                            })

        req.raise_for_status()

        graph = req.json()

        qgraph = QGraph(graph)

        return qgraph

    def update(self, graph: Graph) -> None:
        """
        Update QLattice with learnings from a `Graph`.

        When updated, The QLattice learns to produce better and better QGraphs. This is how a QLattice evolves and narrows in on producing QGraphs with better and better models.

        Without updating, the QLattice will not learn about good models and the QGraphs produced from the QLattice will not contain better models.

        # Select the best Graph from the QGraph and update the QLattice with it's learnings
        >>> graph = qgraph.select(data)[0]
        >>> ql.update(graph)

        Arguments:
            graph -- Graph with learnings worth storing.
        """
        req = requests.post("%s/update" % self.url,
                            headers=self.headers,
                            json=graph._to_dict()
                            )

        req.raise_for_status()

    def _load_qlattice(self):
        req = requests.get(self.url, headers=self.headers)
        req.raise_for_status()

        qlattice = req.json()

        self.width = qlattice['width']
        self.height = qlattice['height']

        self.registers = [Register(reg['celltype'], reg['label'], reg['location']) for reg in qlattice['registers']]

    def reset(self):
        """
        Clear all learnings in this QLattice.

        This is a potentially dangerous action. Think twice before calling this method.
        """
        req = requests.post(f"{self.url}/reset", headers=self.headers)
        req.raise_for_status()

        self._load_qlattice()

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (self.width, self.height, self.url)
