import numpy as np


def random_spin(s0, alpha=0.1):
    """Generate a new random spin based on the original one.

    Parameters
    ----------
    s0: np.ndarray

        The original spin to be changed.

    alpha: float

        Larger alpha, larger the change of the spin. Defaults to 0.1.

    Returns
    -------
    np.ndarray

        New updated spin, normalised to 1.

    """
    delta_s = (2 * np.random.random(3) - 1) * alpha
    s1 = s0 + delta_s
    return s1 / np.linalg.norm(s1)


class Driver:
    """Driver class.

    Driver class does not take any input parameters at initialisation.

    """

    def __init__(self):
        pass

    def drive(self, system, n):
        for _ in range(n):
            # Step 1: gegt initial energy
            E0 = system.energy()
            
            # Step 2: select one spin
            nx, ny = system.s.array.shape[:2]
            i, j = np.random.randint(nx), np.random.randint(ny)
            
            # ignore
            original_spin = system.s.array[i, j].copy()
            
            # Step 3: exchange the spin 
            system.s.array[i, j] = random_spin(system.s.array[i, j], alpha=0.1)
            
            # Step 4: get the new energy
            E1 = system.energy()
            
            if E1 >= E0:  # dont change if the energy increases
                system.s.array[i, j] = original_spin



