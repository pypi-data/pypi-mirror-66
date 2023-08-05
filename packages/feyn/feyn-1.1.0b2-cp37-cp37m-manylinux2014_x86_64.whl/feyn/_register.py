from typing import Tuple

import _feyn


class Register:
    """
    Registers are the main interaction point with the QLattice, IO interfaces.

    Users connect registers with their data concepts, columns in their dataset or stores.

    Arguments:
        celltype {str} -- Either "fixed" or "cat" (float or categorical).
        label {str} -- Name of the register, so that you can find it again later.
                        Usually the column name in your dataset, or the name of the concept this register represents.
        location {tuple(int, int, int)} -- Location in the QLattice.
    """

    def __init__(self, celltype: str, label: str, location:Tuple[int, int, int]):
        """Construct a new 'Register' object."""
        self.celltype = celltype
        self.label = label
        self.location = location

    def to_dict(self):
        """Serialize this object to a dictionary.

        Returns:
            [dict] -- This object as a dictionary.
        """
        return {
            'celltype': self.celltype,
            'label': self.label
        }
