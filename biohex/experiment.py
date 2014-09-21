
from biohex import life

class Experiment(object):
    """
    Provides access to the functions needed to monitor the details 
    of a given experiment.
    """

    world = None

    def __init__(self, world=None):
        Experiment.world = world
        self.world = world

    def probeThermalEnergy(self):
        return int(self.world.thermalDelta)

    def probeTemperature(self):
        return round(self.world.thermalDelta / self.world.area + self.world.ambientTemperature, 3)

    def probeAtoms(self):
        """Return the total number of each atom in the world."""
        atoms = []
        for bit in self.world.bits:
            if len(bit.atoms) > len(atoms):
                for i in range(len(bit.atoms)-len(atoms)):
                    atoms.append(0)
            for i in range(len(bit.atoms)):
                atoms[i] += bit.atoms[i]
        return atoms

    def probeEnthalpy(self):
        """Return the total amount of enthalpy in the world."""
        total = 0
        for bit in self.world.bits:
            total += bit.enthalpy
        return total

    def probeEntropy(self):
        """Return the total amount of entropy in the world."""
        total = 0
        for bit in self.world.bits:
            total += bit.ENTROPY
        return total
