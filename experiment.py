
"""
Provides access to the functions needed to monitor the details 
of a given experiment.
"""

def probeAtoms(world):
    """Return the total number of each atom in the world."""
    atoms = []
    for bit in world.bits:
        if len(bit.atoms) > len(atoms):
            for i in range(len(bit.atoms)-len(atoms)):
                atoms.append(0)
        for i in range(len(bit.atoms)):
            atoms[i] += bit.atoms[i]
    return atoms

def probeEnthalpy(world):
    """Return the total amount of enthalpy in the world."""
    total = 0
    for bit in world.bits:
        total += bit.enthalpy
    return total

def probeEntropy(world):
    """Return the total amount of entropy in the world."""
    total = 0
    for bit in world.bits:
        total += bit.ENTROPY
    return total
