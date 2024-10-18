import numpy as np


class System:
    """System object with the spin configuration and simulation parameters.

    Parameters
    ----------
    s: mcsim.Spins

        Two-dimensional spin field.

    B: Iterable(float)

        External magnetic field (vector), length 3.

    K: numbers.Real

        Uniaxial anisotropy constant.

    u: Iterable(float)

        Uniaxial anisotropy axis, length 3. If ``u`` is not normalised to 1, it
        will be normalised before the calculation of uniaxial anisotropy energy.

    J: numbers.Real

        Exchange energy constant.

    D: numbers.Real

        Dzyaloshinskii-Moriya energy constant.

    """

    def __init__(self, s, B, K, u, J, D):
        self.s = s
        self.J = J
        self.D = D
        self.B = B
        self.K = K
        self.u = u

    def energy(self):
        """Total energy of the system.

        The total energy of the system is the sum of all individual energy terms.

        Returns
        -------
        float

            Total energy of the system.

        """
        return self.zeeman() + self.anisotropy() + self.exchange() + self.dmi()

    
    def zeeman(self):
        # Access the spin field array and magnetic field
        energy = -np.sum(np.dot(self.s.array, self.B))
        return energy 


    def anisotropy(self):
        # normalise the anisotropy axis first
        u_norm = self.u / np.linalg.norm(self.u)

        # compute anisotropy energy for each spin
        dot_products = np.dot(self.s.array, u_norm)  
        energy = -self.K * np.sum(dot_products ** 2)
        return energy

    def exchange(self):
        nx, ny = self.s.array.shape[:2]
        total_energy = 0.0

        # Loop through the lattice and get interactions with right and bottom neighbors
        for i in range(nx):
            for j in range(ny):
                if i + 1 < nx:  # bottom neighbor
                    total_energy += np.dot(self.s.array[i, j], self.s.array[i + 1, j])
                if j + 1 < ny:  # right neighbor
                    total_energy += np.dot(self.s.array[i, j], self.s.array[i, j + 1])

        # total energy scaled by the exchange 
        return -self.J * total_energy





    def dmi(self):
        # Get the spin array
        nx, ny = self.s.array.shape[:2]
        total_energy = 0.0

        for i in range(nx):
            for j in range(ny):
                if i + 1 < nx:  # bottom neighbor

                    r_ij = [1, 0, 0]  # direction between s(i, j) and s(i+1, j)
                    d_ij = self.D * np.array(r_ij)  # DMI vector

                    total_energy += np.dot(d_ij, np.cross(self.s.array[i, j], self.s.array[i + 1, j]))

                if j + 1 < ny:  # right neighbor
                    r_ij = [0, 1, 0]  # direction between s(i, j) and s(i, j+1)
                    d_ij = self.D * np.array(r_ij)

                    total_energy += np.dot(d_ij, np.cross(self.s.array[i, j], self.s.array[i, j + 1]))

        return total_energy