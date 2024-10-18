from setuptools import find_packages, setup

setup(
    name="mcsim",
    version="0.1.0",
    description=(
        "Metropolis-Hastings Monte Carlo simulator"
    ),
    author="Barin Odusi",
    author_email="bo823@ic.ac.uk",
    packages=find_packages(),
    install_requires=["numpy", "pytest", "matplotlib"],

)
