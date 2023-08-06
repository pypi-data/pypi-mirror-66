"""Helper functions that may make it easier to interact with feyn."""
import feyn
from typing import List

def add_registers_from_dataframe(qlattice: feyn.QLattice, df) -> List[feyn.Register]:
    """
    Use columns from a pandas DataFrame as registers in a QLattice.

    This is useful when you have a data-set where you want to map all your columns as features in a QLattice.

    Arguments:
        qlattice -- A QLattice object to add the registers on.
        df -- A Pandas DataFrame with the columns you want to use as features.

    Returns:
        List[Register] -- The registers that was created in the QLattice.
    """
    registers = []
    for col in df.columns:
        if df[col].dtype == object:
            registers.append(qlattice.get_register(col, register_type="cat"))
        else:
            registers.append(qlattice.get_register(col, register_type="fixed"))

    return registers
