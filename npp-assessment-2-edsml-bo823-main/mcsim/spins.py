import numbers
import matplotlib.pyplot as plt
import numpy as np


class Spins:
    """Field of spins on a two-dimensional lattice.

    Each spin is a vector s = (sx, sy, sz). Underlying data structure (``self.array``)
    is a NumPy array (``np.ndarray``) with shape ``(nx, ny, 3)``, where ``nx`` and
    ``ny`` are the number of spins in the x and y directions, respectively, and 3 is for
    three spin (vector) components sx, sy, and sz.

    Parameters
    ----------
    n: Iterable

        Dimensions of a two-dimensional lattice ``n = (nx, ny)``, where ``nx`` and
        ``ny`` is the number of atoms in the x and y directions. Values of ``nx`` and
        ``ny`` must be positive integers.

    value: Iterable

        The value ``(sx, sy, sz)`` initializes all spins in the lattice to have the same
        value. All elements of ``value`` must be real numbers. In general, the values of
        spins do not have the same values, for instance, we can call ``randomise``
        method. Defaults to ``(0, 0, 1)``.

    """

    def __init__(self, n, value=(0, 0, 1)):
        # Checks on input parameters.
        if len(n) != 2:
            raise ValueError(f"Length of n must be 2, not {len(n) = }.")
        if any(i <= 0 or not isinstance(i, int) for i in n):
            raise ValueError("Elements of n must be positive integers.")

        if len(value) != 3:
            raise ValueError(
                f"Length of iterable value must be 3, not {len(value) = }."
            )
        if any(not isinstance(i, numbers.Real) for i in n):
            raise ValueError("Elements of value must be real numbers.")

        self.n = n
        self.array = np.empty((*self.n, 3), dtype=np.float64)
        self.array[..., :] = value  # initialise all spins to have the same value

        # We ensure spins are normalised to 1.
        if not np.isclose(value[0] ** 2 + value[1] ** 2 + value[2] ** 2, 1):
            self.normalise()



        self.array = np.zeros((*n, 3))
        self.nx, self.ny = n
        print(f"Initializing spins with value: {value}")
        self.array[:, :3, :] = (0, 1, 0)
        self.array[:, 3:, :] = (0, 0, 1)
        print(f"Spin array initialized:\n{self.array}")

    @property
    def mean(self):
        # calculate the mean of each spin component sx, sy, sz
        mean_sx = np.mean(self.array[:, :, 0])  
        mean_sy = np.mean(self.array[:, :, 1]) 
        mean_sz = np.mean(self.array[:, :, 2])  
        
        return np.array([mean_sx, mean_sy, mean_sz])
        return np.array([mean_sx, mean_sy, mean_sz])

    def __abs__(self):
        norm = np.sqrt(np.sum(self.array ** 2, axis=2))
        return norm 
    

    def normalise(self):
        """Normalise the magnitude of all spins to 1."""
        self.array = self.array / abs(self)
        

    def randomise(self):
        """Initialise the lattice with random spins.

        Components of each spin are between -1 and 1: -1 <= si <= 1, and all
        spins are normalised to 1.

        """
        self.array = 2 * np.random.random((*self.n, 3)) - 1
        self.normalise()

    def plot(self):
        nx, ny = self.array.shape[:2]
        
        X, Y = np.meshgrid(range(nx), range(ny), indexing='ij')
        
        # x and y components of the spin vectors
        U = self.array[:, :, 0]  # sx components
        V = self.array[:, :, 1]  # sy components
        
        # Plot the spins using quiver (for arrows)
        plt.figure(figsize=(6, 6))
        plt.quiver(X, Y, U, V, angles='xy')
        plt.xlim(-1, nx)
        plt.ylim(-1, ny)
        plt.gca().set_aspect('equal')
        plt.title('Spin Lattice')
        plt.show()
