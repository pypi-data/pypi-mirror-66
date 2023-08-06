# -*- coding: utf-8 -*-

"""
Utilities
=========
Provides several useful utility functions.

"""


# %% IMPORTS
# MPI import
from mpi4pyd import MPI

# All declaration
__all__ = ['rprint']

# Determine MPI size and ranks
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()


# %% FUNCTION DEFINITIONS
# Redefine the print function to include the MPI rank if MPI is used
def rprint(*args, **kwargs):
    """
    Custom :func:`~print` function that prepends the world rank of the MPI
    process that calls it to the message if the size of :obj:`MPI.COMM_WORLD`
    is more than 1.
    Takes the same input arguments as the normal :func:`~print` function.

    """

    # If using MPI (size > 1), prepend rank to message
    if(size > 1):
        args = list(args)
        args.insert(0, "Rank %i:" % (rank))
    print(*args, **kwargs)
