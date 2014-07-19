
def probeAtoms(world):
    atoms = []
    for bit in world.bits:
        if len(bit.atoms) > len(atoms):
            for i in range(len(bit.atoms)-len(atoms)):
                atoms.append(0)
        for i in range(len(bit.atoms)):
            atoms[i] += bit.atoms[i]
    return atoms

def probeEnthalpy(world):
    total = 0
    for bit in world.bits:
        total += bit.enthalpy
    return total

def probeEntropy(world):
    total = 0
    for bit in world.bits:
        total += bit.ENTROPY
    return total
