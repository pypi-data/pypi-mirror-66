from typing import Tuple

import _feyn


class Register:
    """
    Registers are the main interaction point with the QLattice, IO interfaces.

    Users connect registers with their data concepts, columns in their dataset or stores.

    The constructor is for internal use. Registers should always be allocated with the `QLattice.get_register` method.

    Arguments:
        celltype -- Either "fixed" or "cat" (numerical or categorical).
        label -- Name of the register, so that you can find it again later. Usually the column name in your dataset, or the name of the concept this register represents.
        location -- Location in the QLattice.
    """

    def __init__(self, celltype: str, label: str, location:Tuple[int, int, int]):
        """Construct a new 'Register' object."""
        self.celltype = celltype
        self.label = label
        self.location = location

    def to_dict(self) -> dict:
        """Serialize this object to a dictionary.

        Returns:
            [dict] -- This object as a dictionary.
        """
        return {
            'celltype': self.celltype,
            'label': self.label
        }
